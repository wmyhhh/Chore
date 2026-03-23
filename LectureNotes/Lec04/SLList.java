public class SLList {
    private IntNode sentinel;
    private int size;

    public SLList(){
        sentinel = new IntNode(10, null);
        size = 0;
    }
    public SLList(int x){
        sentinel = new IntNode(10, null);
        sentinel.next = new IntNode(x, null);
        size = 1;
    }

    public void addFirst(int x){
        sentinel.next = new IntNode(x, sentinel.next);
        size += 1;
    }

    public int getFirst(){
        return sentinel.next.item;
    }

    public void addLast(int x){
        IntNode p = sentinel;
        if (p.next != null){
            p = p.next;
        }
        p.next = new IntNode(x, null);
        size += 1;
    }
    /*
    private int size(IntNode p){
        if (p == null){
            return 0;
        }else {
            return 1+size(p.next);
        }
    }
    */

    public int size(){
        return size;
    }

    public static void main(String[] args){
        SLList L = new SLList(10);
        L.addFirst(5);
        L.addFirst(15);
        L.addLast((30));
        System.out.println(L.size());
        System.out.println(L.getFirst());
    }
}
