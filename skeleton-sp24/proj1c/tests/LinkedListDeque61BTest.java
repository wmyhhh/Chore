import deque.Deque61B;
import deque.LinkedListDeque61B;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

import static com.google.common.truth.Truth.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

/** Regression tests for the basic deque operations and independent iterators. */
public class LinkedListDeque61BTest {
    @Test
    public void emptyRemovalReturnsNullWithoutChangingSize() {
        Deque61B<Integer> deque = new LinkedListDeque61B<>();
        assertThat(deque.removeFirst()).isNull();
        assertThat(deque.removeLast()).isNull();
        assertThat(deque.size()).isEqualTo(0);
        assertThat(deque.isEmpty()).isTrue();
    }

    @Test
    public void addAtBothEndsPreservesLogicalOrder() {
        Deque61B<Integer> deque = new LinkedListDeque61B<>();
        deque.addLast(2);
        deque.addFirst(1);
        deque.addLast(3);
        deque.addFirst(0);
        assertThat(deque.toList()).containsExactly(0, 1, 2, 3).inOrder();
        assertThat(deque.size()).isEqualTo(4);
        assertThat(deque.isEmpty()).isFalse();
        assertThat(deque.removeFirst()).isEqualTo(0);
        assertThat(deque.removeLast()).isEqualTo(3);
        assertThat(deque.toList()).containsExactly(1, 2).inOrder();
    }

    @Test
    public void singletonRemovalRestoresBothEndsAndAllowsReuse() {
        // Exercise all four combinations of insertion end and removal end.
        for (boolean addAtFront : new boolean[]{true, false}) {
            for (boolean removeAtFront : new boolean[]{true, false}) {
                Deque61B<Integer> deque = new LinkedListDeque61B<>();
                if (addAtFront) {
                    deque.addFirst(7);
                } else {
                    deque.addLast(7);
                }
                Integer removed = removeAtFront ? deque.removeFirst() : deque.removeLast();
                assertThat(removed).isEqualTo(7);
                assertThat(deque.size()).isEqualTo(0);
                assertThat(deque.isEmpty()).isTrue();
                assertThat(deque.toList()).isEmpty();
                deque.addFirst(8);
                deque.addLast(9);
                assertThat(deque.removeLast()).isEqualTo(9);
                assertThat(deque.removeFirst()).isEqualTo(8);
                assertThat(deque.isEmpty()).isTrue();
            }
        }
    }

    @Test
    public void iterativeGetRejectsAllOutOfBoundsIndices() {
        Deque61B<String> deque = new LinkedListDeque61B<>();
        assertThat(deque.get(0)).isNull();
        deque.addLast("A");
        deque.addLast("B");
        for (int index : new int[]{-1, Integer.MIN_VALUE, 2, 3, Integer.MAX_VALUE}) {
            assertThat(deque.get(index)).isNull();
        }
        assertThat(deque.toList()).containsExactly("A", "B").inOrder();
    }

    @Test
    public void recursiveGetRejectsNegativeIndices() {
        Deque61B<String> deque = new LinkedListDeque61B<>();
        deque.addLast("A");
        assertThat(deque.getRecursive(-1)).isNull();
        assertThat(deque.getRecursive(Integer.MIN_VALUE)).isNull();
    }

    @Test
    public void recursiveGetDoesNotWrapAroundSentinel() {
        Deque61B<String> deque = new LinkedListDeque61B<>();
        assertThat(deque.getRecursive(0)).isNull();
        deque.addLast("A");
        deque.addLast("B");
        assertThat(deque.getRecursive(2)).isNull();
        assertThat(deque.getRecursive(3)).isNull();
        assertThat(deque.getRecursive(Integer.MAX_VALUE)).isNull();
    }

    @Test
    public void bothGetMethodsReadWithoutChangingDeque() {
        Deque61B<String> deque = new LinkedListDeque61B<>();
        List<String> expected = List.of("A", "B", "C", "D");
        for (String item : expected) {
            deque.addLast(item);
        }
        for (int index = 0; index < expected.size(); index++) {
            assertThat(deque.get(index)).isEqualTo(expected.get(index));
            assertThat(deque.getRecursive(index)).isEqualTo(expected.get(index));
        }
        assertThat(deque.toList()).containsExactlyElementsIn(expected).inOrder();
        assertThat(deque.size()).isEqualTo(expected.size());
    }

    @Test
    public void toListReturnsAnIndependentList() {
        Deque61B<String> deque = new LinkedListDeque61B<>();
        deque.addLast("A");
        List<String> copy = deque.toList();
        copy.clear();
        assertThat(deque.toList()).containsExactly("A");
        deque.addLast("B");
        assertThat(copy).isEmpty();
    }

    @Test
    public void emptyIteratorIsExhaustedImmediately() {
        Iterator<String> iterator = new LinkedListDeque61B<String>().iterator();
        assertThat(iterator.hasNext()).isFalse();
        assertThrows(NoSuchElementException.class, iterator::next);
    }

    @Test
    public void singletonIteratorReturnsTheElementInsteadOfSentinel() {
        Deque61B<String> deque = new LinkedListDeque61B<>();
        deque.addLast("only");
        Iterator<String> iterator = deque.iterator();
        assertThat(iterator.next()).isEqualTo("only");
        assertThat(iterator.hasNext()).isFalse();
        assertThrows(NoSuchElementException.class, iterator::next);
    }

    @Test
    public void iteratorReturnsEveryElementInOrderWithoutRemovingThem() {
        Deque61B<String> deque = new LinkedListDeque61B<>();
        deque.addLast("A");
        deque.addLast("B");
        deque.addLast("C");
        assertThat(deque).containsExactly("A", "B", "C").inOrder();
        assertThat(deque.toList()).containsExactly("A", "B", "C").inOrder();
        assertThat(deque.size()).isEqualTo(3);
    }

    @Test
    public void hasNextDoesNotAdvanceAndNextWorksWithoutAPrecedingCheck() {
        Deque61B<String> deque = new LinkedListDeque61B<>();
        deque.addLast("A");
        deque.addLast("B");
        Iterator<String> iterator = deque.iterator();
        assertThat(iterator.hasNext()).isTrue();
        assertThat(iterator.hasNext()).isTrue();
        assertThat(iterator.next()).isEqualTo("A");
        assertThat(iterator.next()).isEqualTo("B");
        assertThat(iterator.hasNext()).isFalse();
        assertThrows(NoSuchElementException.class, iterator::next);
        assertThat(iterator.hasNext()).isFalse();
    }

    @Test
    public void iteratorsHaveIndependentCursors() {
        Deque61B<String> deque = new LinkedListDeque61B<>();
        deque.addLast("A");
        deque.addLast("B");
        Iterator<String> first = deque.iterator();
        Iterator<String> second = deque.iterator();
        assertThat(first.next()).isEqualTo("A");
        assertThat(first.next()).isEqualTo("B");
        assertThat(first.hasNext()).isFalse();
        assertThat(second.next()).isEqualTo("A");
        assertThat(second.next()).isEqualTo("B");
        assertThat(deque.iterator().next()).isEqualTo("A");
    }

    @Test
    public void nestedLoopsVisitEveryPair() {
        Deque61B<Integer> deque = new LinkedListDeque61B<>();
        deque.addLast(1);
        deque.addLast(2);
        List<String> pairs = new ArrayList<>();
        for (int left : deque) {
            for (int right : deque) {
                pairs.add(left + ":" + right);
            }
        }
        assertThat(pairs).containsExactly("1:1", "1:2", "2:1", "2:2").inOrder();
    }

    @Test
    public void mixedOperationsMatchAReferenceSequence() {
        Deque61B<Integer> deque = new LinkedListDeque61B<>();
        List<Integer> expected = new ArrayList<>();
        Random random = new Random(61);
        // A fixed seed makes failures reproducible across runs.
        for (int step = 0; step < 1000; step++) {
            int operation = random.nextInt(4);
            int value = random.nextInt(100);
            if (operation == 0) {
                deque.addFirst(value);
                expected.add(0, value);
            } else if (operation == 1) {
                deque.addLast(value);
                expected.add(value);
            } else if (operation == 2) {
                Integer removed = expected.isEmpty() ? null : expected.remove(0);
                assertThat(deque.removeFirst()).isEqualTo(removed);
            } else {
                Integer removed = expected.isEmpty() ? null : expected.remove(expected.size() - 1);
                assertThat(deque.removeLast()).isEqualTo(removed);
            }
            assertThat(deque.size()).isEqualTo(expected.size());
            assertThat(deque.isEmpty()).isEqualTo(expected.isEmpty());
            assertThat(deque.toList()).containsExactlyElementsIn(expected).inOrder();
            assertThat(deque).containsExactlyElementsIn(expected).inOrder();
            int index = random.nextInt(expected.size() + 2) - 1;
            Integer item = index < 0 || index >= expected.size() ? null : expected.get(index);
            assertThat(deque.get(index)).isEqualTo(item);
            assertThat(deque.getRecursive(index)).isEqualTo(item);
        }
    }

    @Test
    public void objectMethodsCompareContentsAndHashEqualDequesAlike() {
        Deque61B<String> first = new LinkedListDeque61B<>();
        Deque61B<String> second = new LinkedListDeque61B<>();
        first.addLast("front");
        first.addLast("back");
        second.addLast("front");
        second.addLast("back");

        // Separate linked lists can represent the same ordered values.
        assertThat(first).isEqualTo(second);
        assertThat(first.hashCode()).isEqualTo(second.hashCode());
        second.removeFirst();
        second.addLast("front");
        assertThat(first).isNotEqualTo(second); // Order matters.
    }

    @Test
    public void objectToStringShowsItemsFromFrontToBack() {
        Deque61B<String> deque = new LinkedListDeque61B<>();
        assertThat(deque.toString()).isEqualTo("[]");
        deque.addLast("front");
        deque.addLast("back");
        assertThat(deque.toString()).isEqualTo("[front, back]");
    }
}
