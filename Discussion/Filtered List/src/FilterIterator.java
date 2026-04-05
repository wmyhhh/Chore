import java.util.Iterator;
import java.util.NoSuchElementException;

public class FilterIterator<T> implements Iterator<T> {
    int pos;

    public FilterIterator(T[] L){
        pos = 0;
        movePos();
    }

    @Override
    public boolean hasNext(){
        return (pos<list.size);
    }

    @Override
    public T next(){
        if (!hasNext()){
            throw new NoSuchElementException();
        }
        T ans = list.get(pos);
        pos++;
        movePos();
        return ans;
    }

    private void movePos(){
        while (hasNext() && !pred.test(list.get(pos))){
            pos ++;
        }
    }
}
