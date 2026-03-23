public class Maximizer {
    public static Comparable max(Comparable[] x){
        int n = 0;
        for (int i=1; i< x.length; i++){
            if (x[i].compareTo(x[n]) > 0){
                n = i;
            }
        }
        return x[n];
    }
}
