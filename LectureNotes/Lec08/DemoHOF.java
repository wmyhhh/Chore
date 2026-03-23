public class DemoHOF {
    public static int doTwice(IntUnaryFunction f, int x){
        return f.apply(f.apply(x));
    }

    public static void main(String[] args){
        IntUnaryFunction f = new TenX();
        IntUnaryFunction g = new AddX();
        System.out.println(doTwice(f, 3));
        System.out.println(doTwice(g, 3));
    }
}
