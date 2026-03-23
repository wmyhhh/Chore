public class GAList<Blarr> {
    public int size;
    public Blarr[] item;

    public GAList(){
        item = (Blarr[]) new Object[100];
        size = 0;
    }

    private void resize(int capacity){
        Blarr[] a = (Blarr[]) new Object[capacity];
        System.arraycopy(item, 0, a, 0, size);
        item = a;
    }

    public void addLast(Blarr i){
        if (size == item.length){
            resize(size * 2);
        }
        item[size] = i;
        size ++;
    }

    public Blarr getLast(){
        return item[size - 1];
    }

    public Blarr removeLast(){
        Blarr x = item[size - 1];
        item[size - 1] = null;
        size --;
        return x;
    }

    public Blarr get(int i){
        return item[i];
    }

    public int size(){
        return size;
    }

    public static void main(String[] args){
        GAList<Integer> L = new GAList<>();
        for (int i=0; i<10000; i ++){
            L.addLast(i);
        }
        System.out.println(L.size());
        System.out.println(L.get(999));

    }
}
