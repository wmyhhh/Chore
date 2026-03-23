public class AList {
    int[] item;
    int size;

    public AList(){
        item = new int[100];
        size = 0;
    }

    public void addLast(int n){
        if (size == item.length){
            resize(size * 2);
        }
        item[size] = n;
        size  += 1;
    }

    public int getLast(){
        return item[size - 1];
    }

    public int removeLast(){
        int x = getLast();
        size --;
        return x;
    }

    public int get(int i){
        return item[i];
    }

    private void resize(int capacity){
        int[] a = new int[capacity];
        System.arraycopy(item, 0, a, 0, size);
        item = a;
    }


    public static void main(String[] args){

    }

}
