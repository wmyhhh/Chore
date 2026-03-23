import java.awt.desktop.SystemEventListener;

public class AList<Item> implements List61B<Item> {
    private Item[] items;
    private int size;

    public AList(){
        size = 0;
        items = (Item[]) new Object[100];
    }

    @Override
    public void insert(Item x, int pos){
        Item[] newItem = (Item[]) new Object[items.length + 1];

        System.arraycopy(items, 0, newItem, 0, pos);

        newItem[pos] = x;

        System.arraycopy(items, pos, newItem, pos +1, items.length - pos);
        items = newItem;

        size ++;
    }

    private void resize(int capacity){
        Item[] a = (Item[]) new Object[capacity];
        System.arraycopy(items, 0, a, 0, size);
        items = a;
    }

    @Override
    public void addFirst(Item x){
        insert(x, 0);
        size ++;
    }

    @Override
    public void addLast(Item x){
        if (size == items.length){
            resize(size * 2);
        }

        items[size] = x;
        size ++;
    }

    @Override
    public Item getFirst(){
        return items[0];
    }

    @Override
    public Item getLast(){
        return items[size - 1];
    }

    @Override
    public Item get(int i){
        return items[i];
    }

    @Override
    public int size(){
        return size;
    }

    @Override
    public Item removeLast(){
        Item x = getLast();
        items[size - 1] = null;
        size --;
        return x;
    }

}
