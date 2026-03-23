import java.util.SequencedSet;

public class SLList<Blorp> implements List61B<Blorp> {
    private class Node {
        private Blorp item;
        private Node next;

        public Node(Blorp i, Node n) {
            item = i;
            next = n;
        }
    }

    public int size;
    public Node sentinel;

    public SLList(){
        size = 0;
        sentinel = new Node(null, null);
    }

    public SLList(Blorp i){
        size = 1;
        sentinel = new Node(null, null);
        sentinel.next = new Node(i, null);
    }

    private Node getNode(int i){
        Node p = sentinel.next;
        while (i > 0 && p.next!= null){
            p = p.next;
            i --;
        }
        return p;
    }

    private Node getLastNode(){
        return getNode(size - 1);
    }

    @Override
    public void insert(Blorp x, int i){
        if (i == 0){
            addFirst(x);
            return;
        }
        Node p = getNode(i - 1);
        p.next = new Node(x, p.next);
        size ++;
    }

    @Override
    public void addFirst(Blorp x){
        sentinel.next = new Node(x, sentinel.next);
        size ++;
    }

    @Override
    public void addLast(Blorp x){
        if (size == 0) {
            sentinel.next = new Node(x, null);
        }else{
        Node p = getLastNode();
        p.next = new Node(x, null);}
        size ++;
    }

    @Override
    public Blorp getFirst(){
        return sentinel.next.item;
    }

    @Override
    public Blorp getLast(){
        return getLastNode().item;
    }

    @Override
    public Blorp get(int i){
        Node p = getNode(i);
        return p.item;
    }

    @Override
    public Blorp removeLast(){
        Node p = getNode(size -  2);
        Blorp x = p.next.item;
        p.next = null;
        size --;
        return x;
    }

    @Override
    public int size(){
        return size;
    }

    @Override
    public void print(){
        Node p = sentinel;
        while (p.next != null){
            p = p.next;
            System.out.print(p.item + " ");
        }
        System.out.println();
    }


    public static void main(String[] args){
        SLList<String> L = new SLList<>();
        L.addFirst("apple");
        L.addFirst("penguin");
        L.addLast("PINGU");
        L.insert("adore", 0);
        L.insert("ABRACRADABRA", 3);
        L.print();
        System.out.println("  ");
        L.removeLast();
        L.addLast("3.14");
        L.print();
    }
}
