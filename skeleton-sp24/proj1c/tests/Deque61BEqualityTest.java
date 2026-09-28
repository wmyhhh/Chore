import deque.ArrayDeque61B;
import deque.Deque61B;
import deque.LinkedListDeque61B;
import org.junit.jupiter.api.Test;

import java.util.HashSet;
import java.util.Set;

import static com.google.common.truth.Truth.assertThat;

/** Checks the shared value-based equality contract of both deque representations. */
public class Deque61BEqualityTest {
    @Test
    public void equalDistinctElementsAndRepresentations() {
        Deque61B<String> array = new ArrayDeque61B<>();
        Deque61B<String> linked = new LinkedListDeque61B<>();
        array.addLast(new String("front"));
        array.addLast(new String("back"));
        linked.addLast(new String("front"));
        linked.addLast(new String("back"));

        assertThat(array.equals(linked)).isTrue();
        assertThat(linked.equals(array)).isTrue();
        assertThat(array.hashCode()).isEqualTo(linked.hashCode());
    }

    @Test
    public void sameRepresentationAlsoUsesElementValues() {
        Deque61B<String> first = new ArrayDeque61B<>();
        Deque61B<String> second = new ArrayDeque61B<>();
        first.addLast(new String("item"));
        second.addLast(new String("item"));
        assertThat(first.equals(second)).isTrue();

        Deque61B<String> third = new LinkedListDeque61B<>();
        Deque61B<String> fourth = new LinkedListDeque61B<>();
        third.addLast(new String("item"));
        fourth.addLast(new String("item"));
        assertThat(third.equals(fourth)).isTrue();
    }

    @Test
    public void orderAndMultiplicityAreSignificant() {
        Deque61B<String> first = new ArrayDeque61B<>();
        Deque61B<String> second = new LinkedListDeque61B<>();
        first.addLast("A");
        first.addLast("B");
        second.addLast("B");
        second.addLast("A");
        assertThat(first.equals(second)).isFalse();
        assertThat(second.equals(first)).isFalse();

        second.removeFirst();
        second.addFirst("A");
        assertThat(first.equals(second)).isFalse();
    }

    @Test
    public void emptySelfNullAndUnrelatedObjects() {
        Deque61B<Integer> array = new ArrayDeque61B<>();
        Deque61B<Integer> linked = new LinkedListDeque61B<>();
        assertThat(array.equals(array)).isTrue();
        assertThat(linked.equals(linked)).isTrue();
        assertThat(array.equals(linked)).isTrue();
        assertThat(linked.equals(array)).isTrue();
        assertThat(array.equals(null)).isFalse();
        assertThat(linked.equals("[]")).isFalse();
    }

    @Test
    public void wrappedAndResizedArrayUsesLogicalOrder() {
        Deque61B<Integer> array = new ArrayDeque61B<>();
        Deque61B<Integer> linked = new LinkedListDeque61B<>();
        for (int value = 0; value < 24; value++) {
            array.addLast(value);
        }
        for (int value = 0; value < 13; value++) {
            array.removeFirst();
        }
        for (int value = 13; value < 24; value++) {
            linked.addLast(value);
        }
        assertThat(array.equals(linked)).isTrue();
        assertThat(linked.equals(array)).isTrue();
        assertThat(array.hashCode()).isEqualTo(linked.hashCode());
    }

    @Test
    public void equalDequesWorkAsHashSetKeys() {
        Deque61B<String> array = new ArrayDeque61B<>();
        Deque61B<String> linked = new LinkedListDeque61B<>();
        array.addLast(new String("same"));
        linked.addLast(new String("same"));

        Set<Deque61B<String>> set = new HashSet<>();
        set.add(array);
        assertThat(set.contains(linked)).isTrue();
    }

    @Test
    public void nullElementsCompareSafelyIfTheyArePresent() {
        Deque61B<String> array = new ArrayDeque61B<>();
        Deque61B<String> linked = new LinkedListDeque61B<>();
        array.addLast(null);
        linked.addLast(null);
        assertThat(array.equals(linked)).isTrue();
        assertThat(linked.equals(array)).isTrue();
        assertThat(array.hashCode()).isEqualTo(linked.hashCode());
    }

    @Test
    public void bothToStringMethodsShowLogicalOrderWithoutChangingContents() {
        Deque61B<String> array = new ArrayDeque61B<>();
        Deque61B<String> linked = new LinkedListDeque61B<>();
        assertThat(array.toString()).isEqualTo("[]");
        assertThat(linked.toString()).isEqualTo("[]");

        for (String value : new String[]{"front", "middle", "back"}) {
            array.addLast(value);
            linked.addLast(value);
        }
        assertThat(array.toString()).isEqualTo("[front, middle, back]");
        assertThat(linked.toString()).isEqualTo("[front, middle, back]");
        assertThat(array.size()).isEqualTo(3);
        assertThat(linked.size()).isEqualTo(3);
    }
}
