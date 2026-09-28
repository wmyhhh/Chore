import jh61b.utils.Reflection;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Field;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import static com.google.common.truth.Truth.assertThat;
import static com.google.common.truth.Truth.assertWithMessage;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class ArrayDeque61BTest {

    @Test
    @DisplayName("ArrayDeque61B has no fields besides backing array and primitives")
    void noNonTrivialFields() {
        List<Field> badFields = Reflection.getFields(ArrayDeque61B.class)
                .filter(f -> !(f.getType().isPrimitive() || f.getType().equals(Object[].class) || f.isSynthetic()))
                .toList();

        assertWithMessage("Found fields that are not array or primitives").that(badFields).isEmpty();
    }

    @Test
    void addAtBothEndsFromEmpty() {
        ArrayDeque61B<Integer> deque = new ArrayDeque61B<>();
        assertThat(deque.isEmpty()).isTrue();
        assertThat(deque.toList()).isEmpty();

        deque.addLast(10);
        assertThat(deque.get(0)).isEqualTo(10);
        deque.addFirst(5);
        deque.addLast(20);

        assertThat(deque.toList()).containsExactly(5, 10, 20).inOrder();
        assertThat(deque.size()).isEqualTo(3);
        assertThat(deque.isEmpty()).isFalse();
    }

    @Test
    void growFromBothEnds() {
        ArrayDeque61B<Integer> fromFront = new ArrayDeque61B<>();
        ArrayDeque61B<Integer> fromBack = new ArrayDeque61B<>();
        for (int i = 0; i < 20; i++) {
            fromFront.addFirst(i);
            fromBack.addLast(i);
        }

        assertThat(fromFront.size()).isEqualTo(20);
        assertThat(fromFront.get(0)).isEqualTo(19);
        assertThat(fromFront.get(19)).isEqualTo(0);
        assertThat(fromBack.size()).isEqualTo(20);
        assertThat(fromBack.get(0)).isEqualTo(0);
        assertThat(fromBack.get(19)).isEqualTo(19);
    }

    @Test
    void getRejectsInvalidLogicalIndices() {
        ArrayDeque61B<String> deque = new ArrayDeque61B<>();
        assertThat(deque.get(0)).isNull();
        deque.addLast("A");
        deque.addLast("B");

        assertThat(deque.get(-1)).isNull();
        assertThat(deque.get(0)).isEqualTo("A");
        assertThat(deque.get(1)).isEqualTo("B");
        assertThat(deque.get(2)).isNull();
        assertThat(deque.get(100)).isNull();
    }

    @Test
    void toListReturnsAnIndependentCopy() {
        ArrayDeque61B<Integer> deque = new ArrayDeque61B<>();
        deque.addFirst(1);
        deque.addLast(2);

        List<Integer> copy = deque.toList();
        copy.clear();

        assertThat(deque.toList()).containsExactly(1, 2).inOrder();
        assertThat(deque.size()).isEqualTo(2);
    }

    @Test
    void removeAtBothEndsAndReuseAfterEmpty() {
        ArrayDeque61B<Integer> deque = new ArrayDeque61B<>();
        assertThat(deque.removeFirst()).isNull();
        assertThat(deque.removeLast()).isNull();

        deque.addFirst(10);
        deque.addLast(20);
        deque.addLast(30);
        assertThat(deque.removeFirst()).isEqualTo(10);
        assertThat(deque.removeLast()).isEqualTo(30);
        assertThat(deque.removeLast()).isEqualTo(20);
        assertThat(deque.isEmpty()).isTrue();
        assertThat(deque.toList()).isEmpty();

        deque.addLast(40);
        deque.addFirst(35);
        assertThat(deque.toList()).containsExactly(35, 40).inOrder();
    }

    @Test
    void shrinkAfterGrowPreservesOrder() {
        ArrayDeque61B<Integer> deque = new ArrayDeque61B<>();
        for (int i = 0; i < 32; i++) {
            deque.addLast(i);
        }
        for (int i = 0; i < 29; i++) {
            assertThat(deque.removeFirst()).isEqualTo(i);
        }

        assertThat(deque.toList()).containsExactly(29, 30, 31).inOrder();
        deque.addFirst(28);
        assertThat(deque.removeLast()).isEqualTo(31);
        assertThat(deque.toList()).containsExactly(28, 29, 30).inOrder();
    }

    @Test
    void getRecursiveIsUnsupportedForArrayDeque() {
        ArrayDeque61B<Integer> deque = new ArrayDeque61B<>();
        assertThrows(UnsupportedOperationException.class, () -> deque.getRecursive(0));
    }

    @Test
    void mixedOperationsMatchStandardLibraryDeque() {
        ArrayDeque61B<Integer> deque = new ArrayDeque61B<>();
        // The standard-library deque is a test oracle, not the implementation.
        ArrayDeque<Integer> expected = new ArrayDeque<>();
        Random random = new Random(61);

        for (int i = 0; i < 2000; i++) {
            int action = random.nextInt(4);
            if (action == 0) {
                deque.addFirst(i);
                expected.addFirst(i);
            } else if (action == 1) {
                deque.addLast(i);
                expected.addLast(i);
            } else if (action == 2) {
                assertThat(deque.removeFirst()).isEqualTo(expected.pollFirst());
            } else {
                assertThat(deque.removeLast()).isEqualTo(expected.pollLast());
            }

            if (i % 25 == 0) {
                assertThat(deque.toList()).isEqualTo(new ArrayList<>(expected));
                assertThat(deque.size()).isEqualTo(expected.size());
            }
        }

        assertThat(deque.toList()).isEqualTo(new ArrayList<>(expected));
    }
}
