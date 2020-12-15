#!/usr/bin/env python3

import sys
import time

from collections import defaultdict
from tabulate import tabulate

import tool.discovery as discovery

from tool.config import CONFIG
from tool.distribution import get_time_distribution
from tool.model import Result, Submission
from tool.runners.wrapper import SubmissionWrapper
from tool.utils import BColor


class DifferentAnswersException(Exception):
    pass


class UnexpectedDebugLinesException(Exception):
    pass


def run(
    days,
    parts,
    authors,
    ignored_authors,
    languages,
    force,
    no_debug,
    all_days_parts,
    restricted,
    expand,
    print_time_dist,
):
    problems = discovery.get_problems(days, parts, all_days_parts)
    printed_day_header = set()
    errors = []

    for problem in problems:
        if problem.day not in printed_day_header:
            printed_day_header.add(problem.day)
            print_day_header(problem)
        print_part_header(problem)

        submissions = discovery.get_submissions(
            problem, authors, ignored_authors, languages, force
        )
        inputs = discovery.get_inputs(problem)

        results_by_author = defaultdict(list)
        results_by_input = defaultdict(list)

        for input in inputs:
            previous = None
            for submission in submissions:
                # The split allows having author.lang and author.x.lang files, on the same input
                if restricted and input.author != submission.author.split(".")[0]:
                    continue
                try:
                    result = run_submission(
                        problem, submission, input, previous, no_debug
                    )
                    results_by_author[submission.author].append(result)
                    results_by_input[input.author].append(result)
                    previous = result
                except DifferentAnswersException as e:
                    errors.append("{}ERROR: {}{}".format(BColor.RED, e, BColor.ENDC))
                except UnexpectedDebugLinesException as e:
                    errors.append("{}ERROR: {}{}".format(BColor.RED, e, BColor.ENDC))

        for submission in submissions:
            submission.runnable.cleanup()
        if problem.parser():
            problem.parser().cleanup()

        if restricted:
            print_restrict_results(problem, results_by_author)
        elif expand:
            print_expanded_results(problem, results_by_input)
        else:
            print_aggregated_results(problem, results_by_author, print_time_dist)

    for err in errors:
        print(err, file=sys.stderr)
    if errors:
        exit(1)


def run_submission(problem, submission, input, previous, no_debug):
    start = time.perf_counter()
    output = submission.runnable.run(input.content)
    end = time.perf_counter()
    msecs = (end - start) * 1000

    # TODO: SubmissionPy and SubmissionWrapper are fairly asymmetrical and need to be unified
    if isinstance(submission.runnable, SubmissionWrapper):
        answer, duration_line, debug_lines = output

        if duration_line is not None:
            msecs = float(duration_line[len("_duration:"):])

        if len(debug_lines) != 0:
            if no_debug:
                raise UnexpectedDebugLinesException(
                    f"unexpected debug lines in {submission.path()}:\n"
                    + "\n".join(debug_lines)
                )
            else:
                print("\n".join(debug_lines))
    else:
        answer = str(output)

    if problem.parser():
        answer = problem.parser().parse(answer)
    if previous is not None and answer != previous.answer:
        raise DifferentAnswersException(
            """different answers day:{} part:{}
input: {}
{}: {}
{}: {}""".format(
                problem.day,
                problem.part,
                input.path(),
                previous.submission.path(),
                previous.answer,
                submission.path(),
                answer,
            )
        )
    return Result(problem, submission, input, answer, msecs)


def print_results(results, print_time_dist=False):
    results.sort(key=lambda x: x.duration)
    print(
        tabulate(
            [
                [
                    "  {color}{author}{end}  ".format(
                        color=(
                            BColor.BOLD
                            if result.submission.author == CONFIG.user
                            else BColor.GREEN
                        ),
                        author=result.submission.author,
                        end=BColor.ENDC,
                    ),
                    "  {color}{answer}{end}  ".format(
                        color=(
                            BColor.BOLD
                            if result.submission.author == CONFIG.user
                            else BColor.BLUE
                        ),
                        answer=result.answer,
                        end=BColor.ENDC,
                    ),
                    "  {color}{msecs:8.3f} ms{end}".format(
                        color=BColor.BOLD, msecs=result.duration, end=BColor.ENDC
                    ),
                    "  {color}{language}{end}".format(
                        color=(
                            BColor.BOLD
                            if result.submission.author == CONFIG.user
                            else ""
                        ),
                        language=result.submission.language,
                        end=BColor.ENDC,
                    ),
                    "  {color}{time_distribution}{end}".format(
                        color=(
                            BColor.BOLD
                            if result.submission.author == CONFIG.user
                            else ""
                        ),
                        time_distribution=get_time_distribution(result.all_durations),
                        end=BColor.ENDC,
                    ) if print_time_dist else None,
                ]
                for result in results
            ]
        )
    )


def print_expanded_results(problem, results_by_input):
    for input_author, submission_results in results_by_input.items():
        print("---------------------------------------------------")
        print(
            "On input from {yellow}{author}{end}".format(
                yellow=BColor.YELLOW, end=BColor.ENDC, author=input_author
            )
        )
        print("---------------------------------------------------")
        results = []
        for result in submission_results:
            results.append(result)
        print_results(results)


def print_restrict_results(problem, results_by_author):
    print("---------------------------------------------------")
    print("On own inputs")
    print("---------------------------------------------------")
    results = []
    for author, results_by_input in results_by_author.items():
        for result in results_by_input:
            results.append(result)
    print_results(results)


def print_aggregated_results(problem, results_by_author, print_time_dist=False):
    print("---------------------------------------------------")
    print("Avg over all inputs")
    print("---------------------------------------------------")
    results = []
    # Loop for all authors, get all the results they produced
    for author, results_by_input in results_by_author.items():
        res_by_language = {}
        count_by_language = defaultdict(int)
        durations_by_language = defaultdict(list)
        # The results can be made by different languages. Make a virtual result (storing total duration) by language
        for result in results_by_input:
            result_language = result.submission.language
            count_by_language[result_language] += 1
            # New language: make the virtual result
            if result_language not in res_by_language:
                res = Result(
                    problem,
                    Submission(problem, author, result_language, init_runnable=False),
                    None,
                    "-",
                    0,
                )
                res_by_language[result_language] = res
            # The author is on his own input, get his answer (split to allow author.x.lang on input author.txt)
            if author.split(".")[0] == result.input.author:
                res_by_language[result_language].answer = result.answer
                res_by_language[result_language].input = result.input
                res_by_language[result_language].submission = result.submission
            # Add up the duration of this result
            res_by_language[result_language].duration += result.duration
            durations_by_language[result_language].append(result.duration)
        # For each language of the author, make the average and store the final result
        for lang, res in res_by_language.items():
            if count_by_language[lang] > 0:
                res.duration /= count_by_language[lang]
            res.all_durations = durations_by_language[result_language]
            results.append(res)
    print_results(results, print_time_dist)


def print_day_header(problem):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(
        BColor.RED
        + BColor.BOLD
        + "Running submissions for day %02d:" % problem.day
        + BColor.ENDC
    )


def print_part_header(problem):
    print(
        "\n" + BColor.MAGENTA + BColor.BOLD + "* part %d:" % problem.part + BColor.ENDC
    )
