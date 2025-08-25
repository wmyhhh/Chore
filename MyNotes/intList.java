public class intList {
    public int first;
    public intList rest;

    public intList(int f, intList r){
        first = f;
        rest = r;
    }

    public int size(){
        if (rest == null){
            return 1;
        }
        return 1 + this.rest.size();
    }

    public int iterativeSize(){
        intList p = this;
        int cnt = 0;
        while (p != null){
            cnt += 1;
            p = p.rest;
        }
        return cnt;
    }

    public int get(int i){
        if (i == 0){
            return first;
        }
        return rest.get(i - 1);
    }
    public static void main(String[] args){
        /**
        intList L = new intList();
        L.first = 5;
        L.rest = null;

        L.rest = new intList();
        L.rest.first = 10;

        L.rest.rest = new intList();
        L.rest.rest.first = 30;
         */
        intList L = new intList(5, null);
        L = new intList(30, L);
        L = new intList(50, L);
        System.out.println(L.size());
        System.out.println(L.iterativeSize());
        System.out.println(L.get(2));
    }

}
