import java.util.Iterator;
import java.util.NoSuchElementException;


public class OHIterator implements Iterator<OHRequest>{
    OHRequest curr;

    public OHIterator(OHRequest queue){
        curr = queue;
    }

    public boolean isGood(String description){
        return description != null && description.length() > 5;
    }

    @Override
    public OHRequest next(){
        if (!hasNext()){
            throw new NoSuchElementException();
        }
        OHRequest x = curr;
        curr = curr.next;
        return x;
    }

    @Override
    public boolean hasNext(){
        while (curr != null && !isGood(curr.description)){
            curr = curr.next;
        }
        if (curr == null){
            return false;
        }
        return true;

    }
}
