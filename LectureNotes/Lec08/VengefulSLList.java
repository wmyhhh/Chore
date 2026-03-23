public class VengefulSLList<Item> extends SLList<Item>{
    public SLList<Item> removed;

    public VengefulSLList(){
        super();
        removed = new SLList<>();
    }

    public VengefulSLList(Item x){
        super(x);
        removed = new SLList<>();
    }

    @Override
    public Item removeLast(){
        Item x = super.removeLast();
        removed.addLast(x);
        return x;
    }
}
