import java.util.*;
public class FilteredList<T> implements Iterable<T> {
    List<T> list;
    Predicate<T> pred;

    public FilteredList(List<T> L, Predicate<T> filter){
        list = L;
        pred = filter;
    }

    @Override
    public Iterator<T> iterator(){
        return new FilterIterator();
    }
}
