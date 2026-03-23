import java.util.Arrays;

public class FillGrid {
    public static void fillGrid(int[] LL, int[] UR, int[][] S){
        int N = S.length;
        int KL, KR;
        KL = KR = 0;

        for (int i = 0; i < N; i ++){
            // fill the LL
            for (int j = 0; j < i; j ++){
                S[i][j] = LL[KL];
                KL ++;
            }

            //fill the UR
            for (int k = i + 1; k < N; k ++){
                S[i][k] = UR[KR];
                KR ++;
            }
        }
    }

    public static void main(String[] args){
        int[] LL = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 0 };
        int[] UR = { 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 };
        int[][] S = {
                { 0, 0, 0, 0, 0},
                { 0, 0, 0, 0, 0},
                { 0, 0, 0, 0, 0},
                { 0, 0, 0, 0, 0},
                { 0, 0, 0, 0, 0}
        };

        fillGrid(LL, UR, S);
        System.out.println(Arrays.deepToString(S));
    }
}
