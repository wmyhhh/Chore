public class DLList<Blarr> {

    private class SomeNode {
        public SomeNode prev;
        public Blarr item;
        public SomeNode next;

        public SomeNode(SomeNode p, Blarr i, SomeNode n){
            prev = p;
            item = i;
            next = n;
        }
    }

    private SomeNode sentinel;
    private int size;

    public DLList(){
        sentinel = new SomeNode(null, null, null);
        sentinel.next = sentinel;
        sentinel.prev = sentinel;
        size = 0;
    }

    public void addFirst(Blarr i){
        SomeNode newNode = new SomeNode(sentinel, i, sentinel.next);
        sentinel.next.prev = newNode;
        sentinel.next = newNode;
        size++;
    }

    public void addLast(Blarr i){
        SomeNode newNode = new SomeNode(sentinel.prev, i, sentinel);
        sentinel.prev.next = newNode;
        sentinel.prev = newNode;
        size++;
    }

    public Blarr getFirst(){
        return sentinel.next.item;
    }

    public Blarr getLast(){
        return sentinel.prev.item;
    }

    public void removeLast(){
        if(size == 0) return;
        sentinel.prev.prev.next = sentinel;
        sentinel.prev = sentinel.prev.prev;
        size--;
    }
}