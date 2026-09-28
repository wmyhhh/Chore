import deque.ArrayDeque61B;
import deque.Deque61B;
import org.junit.jupiter.api.Test;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

import static com.google.common.truth.Truth.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

/** Regression tests for the circular-array representation and its iterator. */
public class ArrayDeque61BTest {
    @Test
    public void emptyOperationsRespectTheContract() {
        Deque61B<Integer> deque = new ArrayDeque61B<>();

        assertThat(deque.isEmpty()).isTrue();
        assertThat(deque.size()).isEqualTo(0);
        assertThat(deque.get(0)).isNull();
        assertThat(deque.get(-1)).isNull();
        assertThat(deque.removeFirst()).isNull();
        assertThat(deque.removeLast()).isNull();
        assertThat(deque.toList()).isEmpty();
    }

    @Test
    public void addAndRemoveAtBothEndsPreserveLogicalOrder() {
        Deque61B<Integer> deque = new ArrayDeque61B<>();
        deque.addLast(2);
        deque.addFirst(1);
        deque.addLast(3);
        deque.addFirst(0);

        assertThat(deque.toList()).containsExactly(0, 1, 2, 3).inOrder();
        assertThat(deque.removeFirst()).isEqualTo(0);
        assertThat(deque.removeLast()).isEqualTo(3);
        assertThat(deque.toList()).containsExactly(1, 2).inOrder();
        assertThat(deque.size()).isEqualTo(2);
    }

    @Test
    public void wrapAroundPreservesLogicalOrder() {
        Deque61B<Integer> deque = new ArrayDeque61B<>();
        for (int item = 0; item < 8; item++) {
            deque.addLast(item);
        }
        for (int item = 0; item < 3; item++) {
            assertThat(deque.removeFirst()).isEqualTo(item);
        }
        for (int item = 8; item < 11; item++) {
            deque.addLast(item);
        }

        assertThat(deque.toList())
                .containsExactly(3, 4, 5, 6, 7, 8, 9, 10)
                .inOrder();
        for (int index = 0; index < deque.size(); index++) {
            assertThat(deque.get(index)).isEqualTo(index + 3);
        }
    }

    @Test
    public void growthAndShrinkPreserveElements() {
        Deque61B<Integer> deque = new ArrayDeque61B<>();
        for (int item = 0; item < 64; item++) {
            deque.addLast(item);
        }
        for (int item = 0; item < 61; item++) {
            assertThat(deque.removeFirst()).isEqualTo(item);
        }

        assertThat(deque.toList()).containsExactly(61, 62, 63).inOrder();
        deque.addFirst(60);
        deque.addLast(64);
        assertThat(deque.toList()).containsExactly(60, 61, 62, 63, 64).inOrder();
    }

    @Test
    public void toListIsAnIndependentCopy() {
        Deque61B<String> deque = new ArrayDeque61B<>();
        deque.addLast("A");
        List<String> copy = deque.toList();

        copy.clear();
        deque.addLast("B");

        assertThat(copy).isEmpty();
        assertThat(deque.toList()).containsExactly("A", "B").inOrder();
    }

    @Test
    public void fullArrayIteratorStopsAfterEveryElement() {
        Deque61B<Integer> deque = new ArrayDeque61B<>();
        for (int item = 0; item < 8; item++) {
            deque.addLast(item);
        }

        assertThat(deque).containsExactly(0, 1, 2, 3, 4, 5, 6, 7).inOrder();
        Iterator<Integer> iterator = deque.iterator();
        for (int expected = 0; expected < 8; expected++) {
            assertThat(iterator.hasNext()).isTrue();
            assertThat(iterator.next()).isEqualTo(expected);
        }
        assertThat(iterator.hasNext()).isFalse();
        assertThrows(NoSuchElementException.class, iterator::next);
    }

    @Test
    public void iteratorsMaintainIndependentPositions() {
        Deque61B<String> deque = new ArrayDeque61B<>();
        deque.addLast("A");
        deque.addLast("B");
        Iterator<String> first = deque.iterator();
        Iterator<String> second = deque.iterator();

        assertThat(first.next()).isEqualTo("A");
        assertThat(first.next()).isEqualTo("B");
        assertThat(first.hasNext()).isFalse();
        assertThat(second.next()).isEqualTo("A");
        assertThat(second.next()).isEqualTo("B");
    }

    @Test
    public void recursiveGetIsExplicitlyUnsupported() {
        Deque61B<Integer> deque = new ArrayDeque61B<>();
        assertThrows(UnsupportedOperationException.class,
                () -> deque.getRecursive(0));
    }

    @Test
    public void mixedOperationsMatchTheStandardLibraryDeque() {
        Deque61B<Integer> actual = new ArrayDeque61B<>();
        ArrayDeque<Integer> expected = new ArrayDeque<>();
        Random random = new Random(61);

        // A fixed seed makes a randomized state-machine test reproducible.
        for (int step = 0; step < 5000; step++) {
            int operation = random.nextInt(4);
            if (operation == 0) {
                actual.addFirst(step);
                expected.addFirst(step);
            } else if (operation == 1) {
                actual.addLast(step);
                expected.addLast(step);
            } else if (operation == 2) {
                assertThat(actual.removeFirst()).isEqualTo(expected.pollFirst());
            } else {
                assertThat(actual.removeLast()).isEqualTo(expected.pollLast());
            }

            List<Integer> expectedList = new ArrayList<>(expected);
            assertThat(actual.size()).isEqualTo(expected.size());
            assertThat(actual.isEmpty()).isEqualTo(expected.isEmpty());
            assertThat(actual.toList()).containsExactlyElementsIn(expectedList).inOrder();
            assertThat(actual).containsExactlyElementsIn(expectedList).inOrder();
        }
    }

    @Test
    public void objectMethodsCompareContentsAndHashEqualDequesAlike() {
        Deque61B<String> first = new ArrayDeque61B<>();
        Deque61B<String> second = new ArrayDeque61B<>();
        first.addLast("front");
        first.addLast("back");
        second.addLast("front");
        second.addLast("back");

        // Distinct deque objects with the same logical sequence are equal.
        assertThat(first).isEqualTo(second);
        assertThat(first.hashCode()).isEqualTo(second.hashCode());
        second.removeFirst();
        second.addLast("front");
        assertThat(first).isNotEqualTo(second); // Order matters.
    }

    @Test
    public void objectToStringShowsItemsFromFrontToBack() {
        Deque61B<String> deque = new ArrayDeque61B<>();
        assertThat(deque.toString()).isEqualTo("[]");
        deque.addLast("front");
        deque.addLast("back");
        assertThat(deque.toString()).isEqualTo("[front, back]");
    }
}
