public class IntList {
    public int first;
    public IntList rest;

    public IntList(int f, IntList r) {
        first = f;
        rest = r;
    }

    public static void evenOdd(IntList lst) {
        if (lst == null || lst.rest == null) {
            return;
        }
        IntList even = lst;
        IntList odd = lst.rest;
        IntList oddHead = odd;

        while (odd != null && odd.rest != null){
            even.rest = odd.rest;
            even = even.rest;

            odd.rest = even.rest;
            odd = odd.rest;
        }

        even.rest = oddHead;
    }

    public static void main(String[] args){
        IntList L = new IntList(6, null);
        L = new IntList(5, L);
        L = new IntList(4, L);
        L = new IntList(3, L);
        L = new IntList(2, L);
        L = new IntList(1, L);

        evenOdd(L);
    }
}