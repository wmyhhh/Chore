import java.util.*;

public class ArraySet<T> implements Iterable<T>{
    private T[] items;
    private int size;

    public ArraySet() {
        items = (T[]) new Object[100];
        size = 0;
    }

    /* Returns true if this map contains a mapping for the specified key.
     */
    public boolean contains(T x) {
        for (int i=0; i<size; i++){
            if (x.equals(items[i])){  // IMPORTANT: cannot use "=="
                return true;
            }
        }
        return false;
    }

    /* Associates the specified value with the specified key in this map.
       Throws an IllegalArgumentException if the key is null. */
    public void add(T x) {
        if (contains(x)){
            return;
        }
        if (x == null){
            return;
            //throw new IllegalArgumentException("cannot add null");
        }
        items[size] = x;
        size ++;
    }

    /* Returns the number of key-value mappings in this map. */
    public int size() {
        return size;
    }

    @Override
    /*
    public String toString(){
        String output = "[";
        for (T i: this){
            output += i.toString() + ", ";
        }
        output += "]";
        return output;
    }
    */
    public String toString(){
        List<String> s = new ArrayList<>();
        for (T i: this){
            s.add(i.toString());
        }
        return "{" + String.join(", ", s) + "}";
    }

    public static <gaga> ArraySet<gaga> of(gaga... stuff){
        ArraySet<gaga> s = new ArraySet<>();
        for (gaga i: stuff){
            s.add(i);
        }
        return s;
    }

    @Override
    public boolean equals(Object o){
        if (this == o){
            return true;
        }
        if (o instanceof ArraySet osa){
            if (this.size != osa.size){
                return false;
            }else{
                for (T i: this){
                    if (!osa.contains(i)){
                        return false;
                    }
                }
                return true;
            }
        }
        return false;
    }

    public Iterator<T> iterator(){
        return new ArraySetIterator();
    }

    private class ArraySetIterator implements Iterator<T>{
        private int wizPos;

        public ArraySetIterator(){
            wizPos = 0;
        }

        public boolean hasNext(){
            return wizPos < size;
        }

        public T next(){
            T nextItem = items[wizPos];
            wizPos ++;
            return nextItem;
        }
    }

    public static void main(String[] args) {
        ArraySet<String> s = new ArraySet<>();
        s.add(null);
        s.add("horse");
        s.add("fish");
        s.add("house");
        s.add("fish");
        System.out.println(s.contains("horse"));
        System.out.println(s.size());

        Set<Integer> s2 = new HashSet<>();
        s2.add(2);
        s2.add(5);
        s2.add(10);

        for (String i: s){
            System.out.println(i);
        }

        System.out.println("test toString:  " + s);

        Iterator<String> seer = s.iterator();
        while(seer.hasNext()){
            String x = seer.next();
            System.out.println(x);
        }

        ArraySet<String> s3 = ArraySet.of("a", "big", "piggie");
        System.out.println(s3);
    }
}

    /* Also to do:
    1. Make ArraySet implement the Iterable<T> interface.
    2. Implement a toString method.
    3. Implement an equals() method.
    */