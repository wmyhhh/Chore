import org.junit.jupiter.api.Test;

import static com.google.common.truth.Truth.assertThat;

/** Performs some basic linked list tests. */
public class LinkedListDeque61BTest {

     @Test
     /** In this test, we have three different assert statements that verify that addFirst works correctly. */
     public void addFirstTestBasic() {
         Deque61B<String> lld1 = new LinkedListDeque61B<>();

         lld1.addFirst("back"); // after this call we expect: ["back"]
         assertThat(lld1.toList()).containsExactly("back").inOrder();

         lld1.addFirst("middle"); // after this call we expect: ["middle", "back"]
         assertThat(lld1.toList()).containsExactly("middle", "back").inOrder();

         lld1.addFirst("front"); // after this call we expect: ["front", "middle", "back"]
         assertThat(lld1.toList()).containsExactly("front", "middle", "back").inOrder();

         /* Note: The first two assertThat statements aren't really necessary. For example, it's hard
            to imagine a bug in your code that would lead to ["front"] and ["front", "middle"] failing,
            but not ["front", "middle", "back"].
          */
     }

     @Test
     /** In this test, we use only one assertThat statement. IMO this test is just as good as addFirstTestBasic.
      *  In other words, the tedious work of adding the extra assertThat statements isn't worth it. */
     public void addLastTestBasic() {
         Deque61B<String> lld1 = new LinkedListDeque61B<>();

         lld1.addLast("front"); // after this call we expect: ["front"]
         lld1.addLast("middle"); // after this call we expect: ["front", "middle"]
         lld1.addLast("back"); // after this call we expect: ["front", "middle", "back"]
         assertThat(lld1.toList()).containsExactly("front", "middle", "back").inOrder();
     }

     @Test
     /** This test performs interspersed addFirst and addLast calls. */
     public void addFirstAndAddLastTest() {
         Deque61B<Integer> lld1 = new LinkedListDeque61B<>();

         /* I've decided to add in comments the state after each call for the convenience of the
            person reading this test. Some programmers might consider this excessively verbose. */
         lld1.addLast(0);   // [0]
         lld1.addLast(1);   // [0, 1]
         lld1.addFirst(-1); // [-1, 0, 1]
         lld1.addLast(2);   // [-1, 0, 1, 2]
         lld1.addFirst(-2); // [-2, -1, 0, 1, 2]

         assertThat(lld1.toList()).containsExactly(-2, -1, 0, 1, 2).inOrder();
     }

    // Below, you'll write your own tests for LinkedListDeque61B.
    @Test
    public void sizeAndIsEmptyTest() {
        Deque61B<Integer> deque = new LinkedListDeque61B<>();

        assertThat(deque.size()).isEqualTo(0);
        assertThat(deque.isEmpty()).isTrue();

        deque.addFirst(2);
        assertThat(deque.size()).isEqualTo(1);
        assertThat(deque.isEmpty()).isFalse();

        deque.addFirst(4);
        deque.addLast(0);
        assertThat(deque.size()).isEqualTo(3);

        deque.removeFirst();
        deque.removeLast();
        assertThat(deque.size()).isEqualTo(1);

        deque.removeLast();
        assertThat(deque.size()).isEqualTo(0);
        assertThat(deque.isEmpty()).isTrue();
    }

    @Test
    public void getTest() {
        Deque61B<String> deque = new LinkedListDeque61B<>();

        assertThat(deque.get(0)).isNull();

        deque.addLast("front");
        deque.addLast("middle");
        deque.addLast("back");

        assertThat(deque.get(0)).isEqualTo("front");
        assertThat(deque.get(1)).isEqualTo("middle");
        assertThat(deque.get(2)).isEqualTo("back");
        assertThat(deque.get(-1)).isNull();
        assertThat(deque.get(3)).isNull();
        assertThat(deque.get(1000)).isNull();
        assertThat(deque.toList()).containsExactly("front", "middle", "back").inOrder();
        assertThat(deque.size()).isEqualTo(3);
    }

    @Test
    public void getRecursiveTest() {
        Deque61B<String> deque = new LinkedListDeque61B<>();

        assertThat(deque.getRecursive(0)).isNull();

        deque.addLast("front");
        deque.addLast("middle");
        deque.addLast("back");

        assertThat(deque.getRecursive(0)).isEqualTo("front");
        assertThat(deque.getRecursive(1)).isEqualTo("middle");
        assertThat(deque.getRecursive(2)).isEqualTo("back");
        assertThat(deque.getRecursive(-1)).isNull();
        assertThat(deque.getRecursive(3)).isNull();
        assertThat(deque.getRecursive(1000)).isNull();

        // A lookup is a query, so it must not change the deque.
        assertThat(deque.toList()).containsExactly("front", "middle", "back").inOrder();
        assertThat(deque.size()).isEqualTo(3);
    }

    @Test
    public void removeFirstAndRemoveLastTest() {
        Deque61B<String> deque = new LinkedListDeque61B<>();

        // Removing from an empty deque returns null and preserves empty state.
        assertThat(deque.removeFirst()).isNull();
        assertThat(deque.removeLast()).isNull();
        assertThat(deque.size()).isEqualTo(0);
        assertThat(deque.isEmpty()).isTrue();

        deque.addLast("front");
        deque.addLast("middle");
        deque.addLast("back");

        assertThat(deque.removeFirst()).isEqualTo("front");
        assertThat(deque.toList()).containsExactly("middle", "back").inOrder();
        assertThat(deque.size()).isEqualTo(2);

        assertThat(deque.removeLast()).isEqualTo("back");
        assertThat(deque.toList()).containsExactly("middle");
        assertThat(deque.size()).isEqualTo(1);

        assertThat(deque.removeFirst()).isEqualTo("middle");
        assertThat(deque.toList()).isEmpty();
        assertThat(deque.size()).isEqualTo(0);
        assertThat(deque.isEmpty()).isTrue();

        // Reusing the deque verifies that singleton removal restores the sentinel topology.
        deque.addFirst("again");
        assertThat(deque.removeLast()).isEqualTo("again");
        assertThat(deque.isEmpty()).isTrue();
    }
}
