package deque;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Objects;

public class LinkedListDeque61B<T> implements Deque61B<T> {
    // Hide representation details; inner classes can still access these fields.
    private final Node sentinel;
    private int size;

    private class Node {
        private T item;
        private Node prev;
        private Node next;

        private Node(T i, Node p, Node n) {
            item = i;
            prev = p;
            next = n;
        }
    }

    public LinkedListDeque61B() {
        // An empty circular list points back to its sentinel in both directions.
        sentinel = new Node(null, null, null);
        sentinel.prev = sentinel;
        sentinel.next = sentinel;
        size = 0;
    }

    @Override
    public void addFirst(T x) {
        Node temp = sentinel.next;
        sentinel.next = new Node(x, sentinel, temp);
        temp.prev = sentinel.next;
        size++;
    }

    @Override
    public void addLast(T x) {
        Node temp = sentinel.prev;
        sentinel.prev = new Node(x, temp, sentinel);
        temp.next = sentinel.prev;
        size++;
    }

    @Override
    public List<T> toList() {
        List<T> result = new ArrayList<>();
        Node cursor = sentinel.next;
        while (cursor != sentinel) {
            result.add(cursor.item);
            cursor = cursor.next;
        }
        return result;
    }

    @Override
    public boolean isEmpty() {
        return sentinel.next == sentinel;
    }

    @Override
    public int size() {
        return size;
    }

    @Override
    public T removeFirst() {
        if (isEmpty()) {
            // Deque61B requires null for empty removal, unlike Iterator.next().
            return null;
        }
        T x = sentinel.next.item;
        sentinel.next = sentinel.next.next;
        sentinel.next.prev = sentinel;
        size--;
        return x;
    }

    @Override
    public T removeLast() {
        if (isEmpty()) {
            // Preserve the empty deque and its size when there is nothing to remove.
            return null;
        }
        T x = sentinel.prev.item;
        sentinel.prev = sentinel.prev.prev;
        sentinel.prev.next = sentinel;
        size--;
        return x;
    }

    @Override
    public T get(int index) {
        // Both bounds matter: a negative index must not return the first element.
        if (index < 0 || index >= size) {
            return null;
        }
        int cnt = 0;
        Node cursor = sentinel.next;
        while (cnt < index) {
            cnt++;
            cursor = cursor.next;
        }
        return cursor.item;
    }

    @Override
    public T getRecursive(int index) {
        // Validate before recursion: circular links never terminate at null.
        if (index < 0 || index >= size) {
            return null;
        }
        return getRecursiveHelper(sentinel.next, index);
    }

    private T getRecursiveHelper(Node current, int remaining) {
        // current is a real element; remaining counts links to the target node.
        if (remaining == 0) {
            return current.item;
        }
        return getRecursiveHelper(current.next, remaining - 1);
    }

    @Override
    public Iterator<T> iterator() {
        // Each iterator has its own cursor and shares this deque's nodes.
        return new LinkedListIterator();
    }

    private class LinkedListIterator implements Iterator<T> {
        // Invariant: cursor is the NEXT node to return, or sentinel when exhausted.
        // This inner object can access its enclosing deque's private sentinel.
        private Node cursor = sentinel.next;

        @Override
        public boolean hasNext() {
            return cursor != sentinel;
        }

        @Override
        public T next() {
            if (!hasNext()) {
                // The Iterator contract requires an exception after exhaustion.
                throw new NoSuchElementException();
            }
            T item = cursor.item;
            cursor = cursor.next;
            return item;
        }
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        // Compare through the shared interface so a linked and an array deque
        // can be equal when they contain the same items in the same order.
        if (!(obj instanceof Deque61B<?> otherDeque) || size != otherDeque.size()) {
            return false;
        }

        // Ask the other deque for its iterator; its private iterator class is
        // an implementation detail that this class does not need to construct.
        Iterator<?> otherItems = otherDeque.iterator();
        for (T item : this) {
            if (!Objects.equals(item, otherItems.next())) {
                return false;
            }
        }
        return true;
    }

    @Override
    public int hashCode() {
        // Equal sequences must produce equal hashes across both implementations.
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
