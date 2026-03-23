public class RotateSLList<Item> extends SLList<Item> {
    public void rotate(){
        Item x = removeLast();
        addFirst(x);
    }
}
