import java.util.ArrayList;
import java.util.List;

import static java.lang.Math.floorMod;

public class ArrayDeque61B<T> implements Deque61B<T> {
    // This is the backing array, not a java.util.List.
    private T[] list;
    private int size;
    // These are insertion positions, not positions of existing elements.
    private int nextFirst;
    private int nextLast;

    private int wrap(int index) {
        return floorMod(index, list.length);
    }

    private int toPhysical(int index) {
        // Logical index 0 is one step to the right of nextFirst.
        return wrap(nextFirst + 1 + index);
    }

    @SuppressWarnings("unchecked")
    private void resize(int capacity) {
        T[] temp = (T[]) new Object[capacity];

        // Copy in logical order while toPhysical still uses the old array.
        for (int i = 0; i < size; i++) {
            temp[i] = list[toPhysical(i)];
        }

        list = temp;
        // The copied elements occupy [0, size), so the adjacent insertion
        // positions are immediately before index 0 and after index size - 1.
        nextFirst = capacity - 1;
        nextLast = size;
    }

    @SuppressWarnings("unchecked")
    public ArrayDeque61B() {
        list = (T[]) new Object[8];
        // Empty has no front or back. Choose adjacent insertion positions:
        // addFirst writes index 0; addLast writes index 1.
        nextFirst = 0;
        nextLast = 1;
        size = 0;
    }

    @Override
    public void addFirst(T x) {
        if (size == list.length) {
            resize(list.length * 2);
        }

        list[nextFirst] = x;
        nextFirst = wrap(nextFirst - 1);
        size++;
    }

    @Override
    public void addLast(T x) {
        if (size == list.length) {
            resize(list.length * 2);
        }

        list[nextLast] = x;
        nextLast = wrap(nextLast + 1);
        size++;
    }

    @Override
    public List<T> toList() {
        List<T> newList = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            newList.add(list[toPhysical(i)]);
        }
        return newList;
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
    public T removeFirst() {
        if (isEmpty()) {
            return null;
        }

        // Check usage before removing, as required by this project's spec.
        if (list.length >= 16 && size <= list.length / 4) {
            resize(list.length / 2);
        }

        // Move from the empty insertion position onto the old front element.
        nextFirst = wrap(nextFirst + 1);
        T item = list[nextFirst];
        list[nextFirst] = null; // Release the deque's reference to the removed item.
        size--;
        return item;
    }

    @Override
    public T removeLast() {
        if (isEmpty()) {
            return null;
        }

        if (list.length >= 16 && size <= list.length / 4) {
            resize(list.length / 2);
        }

        // Move from the empty insertion position onto the old back element.
        nextLast = wrap(nextLast - 1);
        T item = list[nextLast];
        list[nextLast] = null; // Release the deque's reference to the removed item.
        size--;
        return item;
    }

    @Override
    public T get(int index) {
        if (index < 0 || index >= size) {
            return null;
        }
        return list[toPhysical(index)];
    }

    @Override
    public T getRecursive(int index) {
        // Project 1B explicitly does not require recursive array access.
        throw new UnsupportedOperationException("No need to implement getRecursive for proj 1b");
    }
}
