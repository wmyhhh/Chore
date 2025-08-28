public class SLList {
    /** shouldn't mess with first*/
    private intNode sentinel;
    private int size;

    /** subordinate class*/
    private static class intNode {      // nested class definition
        // private static class can never use outside instance variable
        // result in a minor savings of memory
        public int item;
        public intNode next;
        public intNode(int i, intNode n){
            item = i;
            next = n;
        }
    }

    public SLList(){
        sentinel = new intNode(42, null);
        size = 0;
    }

    public SLList(int x){
        sentinel = new intNode(42, new intNode(x, null));
    }
    public void addFirst(int x){
        sentinel.next = new intNode(x, sentinel.next);
        size += 1;
    }
    public int getFirst(){
        return sentinel.next.item;
    }
    public void addLast(int x){
        intNode p = sentinel.next;
        while (p.next != null){
            p = p.next;
        }
        p.next = new intNode(x, null);
        size += 1;
    }
    /** helper method: return the size of the list that starts at p
    private static int size(intNode p){
        if(p.next == null){
            return 1;
        }
        else{
            return 1 + size(p.next);
        }
    }
     */
    public int size(){
        //return size(first);
        return size;
    }
    public static void main(String[] args){
        SLList L = new SLList(10);
        L.addFirst(15);
        L.addFirst(5);
        L.addLast(5);
        System.out.println(L.size());
    }
}
