import java.util.ArrayList;
import java.util.List;

public class LinkedListDeque61B<T> implements Deque61B<T> {
    private Node sentinel;
    private int size;

    private class Node {
        private Node prev;
        private T item;
        private Node next;

        private Node(T item, Node prev, Node next) {
            this.item = item;
            this.next = next;
            this.prev = prev;
        }
    }

    public LinkedListDeque61B() {
        // An empty circular deque has a sentinel that points to itself.
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
    public boolean isEmpty() {
        return size == 0;
    }

    @Override
    public int size() {
        return size;
    }

    @Override
    public T removeFirst() {
        // Empty removal follows the interface contract and leaves state unchanged.
        if (isEmpty()) {
            return null;
        }

        Node first = sentinel.next;
        sentinel.next = first.next;
        sentinel.next.prev = sentinel;
        size--;
        return first.item;
    }

    @Override
    public T removeLast() {
        // Empty removal follows the interface contract and leaves state unchanged.
        if (isEmpty()) {
            return null;
        }

        Node last = sentinel.prev;
        sentinel.prev = last.prev;
        sentinel.prev.next = sentinel;
        size--;
        return last.item;
    }

    @Override
    public T get(int index) {
        // Circular links cannot reveal an invalid index, so validate it first.
        if (index < 0 || index >= size) {
            return null;
        }

        Node pointer = sentinel.next;
        for (int i = 0; i < index; i++) {
            pointer = pointer.next;
        }
        return pointer.item;
    }

    @Override
    public T getRecursive(int index) {
        if (index < 0 || index >= size) {
            return null;
        }
        return getRecursiveHelper(sentinel.next, index);
    }

    /** Recurses with local traversal state, leaving the deque unchanged. */
    private T getRecursiveHelper(Node current, int remaining) {
        if (remaining == 0) {
            return current.item;
        }
        return getRecursiveHelper(current.next, remaining - 1);
    }

    @Override
    public List<T> toList() {
        List<T> returnList = new ArrayList<>();
        // A single traversal visits each data node exactly once: Theta(n).
        Node current = sentinel.next;
        while (current != sentinel) {
            returnList.add(current.item);
            current = current.next;
        }
        return returnList;
    }

}
