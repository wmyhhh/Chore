package deque;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Objects;

/** A resizable, circular-array implementation of the {@link Deque61B} interface. */
public class ArrayDeque61B<T> implements Deque61B<T> {
    private static final int INITIAL_CAPACITY = 8;
    private static final int RESIZE_FACTOR = 2;
    private static final int MIN_SHRINK_CAPACITY = 16;

    /*
     * Representation invariants:
     * 1. size is the number of logical elements and is in [0, items.length].
     * 2. nextFirst and nextLast are the boundary slots used by the next insertions;
     *    they are empty whenever the backing array is not full.
     * 3. Logical element i is stored at physicalIndex(i).
     */
    private T[] items;
    private int size;
    private int nextFirst;
    private int nextLast;

    @SuppressWarnings("unchecked")
    public ArrayDeque61B() {
        size = 0;
        items = (T[]) new Object[INITIAL_CAPACITY];
        nextFirst = 0;
        nextLast = 1;
    }

    /** Returns a valid backing-array index for any positive or negative index. */
    private int wrap(int index) {
        return Math.floorMod(index, items.length);
    }

    /** Converts a logical deque index into its backing-array index. */
    private int physicalIndex(int index) {
        return wrap(index + nextFirst + 1);
    }

    @SuppressWarnings("unchecked")
    private void resize(int capacity) {
        if (capacity < size || capacity < INITIAL_CAPACITY) {
            throw new IllegalArgumentException("capacity cannot hold the deque");
        }

        T[] resized = (T[]) new Object[capacity];
        for (int index = 0; index < size; index++) {
            // Copy in logical order so the resized representation is contiguous.
            resized[index] = items[physicalIndex(index)];
        }
        items = resized;
        nextFirst = capacity - 1;
        nextLast = size;
    }

    /** Shrinks geometrically while preserving the minimum capacity of eight. */
    private void shrinkIfNeeded() {
        if (items.length >= MIN_SHRINK_CAPACITY
                && size < items.length / 4) {
            resize(items.length / RESIZE_FACTOR);
        }
    }

    @Override
    public boolean isEmpty() {
        return size == 0;
    }

    @Override
    public int size() {
        return size;
    }

    @Override
    public void addFirst(T x) {
        if (size == items.length) {
            resize(RESIZE_FACTOR * items.length);
        }
        items[nextFirst] = x;
        nextFirst = wrap(nextFirst - 1);
        size++;
    }

    @Override
    public void addLast(T x) {
        if (size == items.length) {
            resize(RESIZE_FACTOR * items.length);
        }
        items[nextLast] = x;
        nextLast = wrap(nextLast + 1);
        size++;
    }

    @Override
    public T removeFirst() {
        if (isEmpty()) {
            return null;
        }

        int first = wrap(nextFirst + 1);
        T removed = items[first];
        // Clear the stale reference so the removed object can be garbage-collected.
        items[first] = null;
        nextFirst = first;
        size--;
        shrinkIfNeeded();
        return removed;
    }

    @Override
    public T removeLast() {
        if (isEmpty()) {
            return null;
        }

        int last = wrap(nextLast - 1);
        T removed = items[last];
        items[last] = null;
        nextLast = last;
        size--;
        shrinkIfNeeded();
        return removed;
    }

    @Override
    public T get(int index) {
        if (index < 0 || index >= size) {
            return null;
        }
        return items[physicalIndex(index)];
    }

    @Override
    public List<T> toList() {
        List<T> result = new ArrayList<>(size);
        for (int index = 0; index < size; index++) {
            result.add(items[physicalIndex(index)]);
        }
        return result;
    }

    @Override
    public T getRecursive(int index) {
        throw new UnsupportedOperationException(
                "getRecursive is not supported by ArrayDeque61B");
    }

    @Override
    public Iterator<T> iterator() {
        // Every call creates an iterator with independent traversal state.
        return new ArrayDequeIterator();
    }

    /*
     * A non-static inner class is appropriate here: every iterator is attached
     * to one enclosing deque and can call its private get method directly.
     */
    private class ArrayDequeIterator implements Iterator<T> {
        // position is a logical index, independent of the circular layout.
        private int position = 0;

        @Override
        public boolean hasNext() {
            return position < size;
        }

        @Override
        public T next() {
            if (!hasNext()) {
                throw new NoSuchElementException();
            }
            T item = get(position);
            position++;
            return item;
        }
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        // Equality is defined by the Deque61B contract, not the backing array.
        if (!(obj instanceof Deque61B<?> otherDeque) || size != otherDeque.size()) {
            return false;
        }

        Iterator<?> otherItems = otherDeque.iterator();
        for (T item : this) {
            // Different references may represent equal values; handle null safely.
            if (!Objects.equals(item, otherItems.next())) {
                return false;
            }
        }
        return true;
    }

    @Override
    public int hashCode() {
        // Both deque implementations must hash the same logical sequence alike.
        int result = 1;
        for (T item : this) {
            result = 31 * result + Objects.hashCode(item);
        }
        return result;
    }

    @Override
    public String toString(){
        List<T> newList = new ArrayList<>();
        for (T x: this) newList.add(x);
        return newList.toString();
    }

}
