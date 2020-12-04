import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;

class Solution {
    // BEWARE: your main class MUST be named Solution

    private static String solve(String input) {
        String[] strList = input.split("\n");
        ArrayList<Integer> intList = new ArrayList<Integer>();
        for (String s: strList) {
            intList.add(Integer.valueOf(s));
        }
        int pos_i = 0;
        int pos_j = 0;
        boolean break_ = false;
        for (int i=0; i<intList.size(); i++) {
            for (int j=0; j<intList.size(); j++) {
                if (intList.get(i) + intList.get(j) == 2020) {
                    break_ = true;
                    pos_i = i;
                    pos_j = j;
                    break;
                }
            }
            if (break_) {
                break;
            }
        }
        return Integer.toString(intList.get(pos_i) * intList.get(pos_j));
    };

    public static void main(String[] args) {
        String input = args[0];
        long startTime = System.currentTimeMillis();
        String result = solve(input);
        System.out.println("_duration: " + (System.currentTimeMillis() - startTime) + "\n" + result);
    }
}
