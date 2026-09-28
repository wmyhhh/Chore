package deque;

import java.util.Comparator;
import java.util.Iterator;
import java.util.Objects;

/** An ArrayDeque61B that can find its largest item using a Comparator. */
public class MaxArrayDeque61B<T> extends ArrayDeque61B<T> {
    private final Comparator<T> comparator;

    public MaxArrayDeque61B(Comparator<T> c) {
        // The comparator is this deque's default ordering for max().
        comparator = Objects.requireNonNull(c, "comparator");
    }

    public T max() {
        return max(comparator);
    }

    public T max(Comparator<T> c) {
        Objects.requireNonNull(c, "comparator");
        Iterator<T> items = iterator();
        if (!items.hasNext()) {
            return null;
        }

        T largest = items.next();
        while (items.hasNext()) {
            T candidate = items.next();
            if (c.compare(candidate, largest) > 0) {
                largest = candidate;
            }
        }
        return largest;
    }
}
