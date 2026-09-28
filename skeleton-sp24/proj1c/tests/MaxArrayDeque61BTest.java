import org.junit.jupiter.api.Test;

import java.util.Comparator;
import deque.MaxArrayDeque61B;

import static com.google.common.truth.Truth.assertThat;

public class MaxArrayDeque61BTest {
    private static class StringLengthComparator implements Comparator<String> {
        public int compare(String a, String b) {
            return a.length() - b.length();
        }
    }

    @Test
    public void basicTest() {
        MaxArrayDeque61B<String> mad = new MaxArrayDeque61B<>(new StringLengthComparator());
        mad.addFirst("");
        mad.addFirst("2");
        mad.addFirst("fury road");
        assertThat(mad.max()).isEqualTo("fury road");
    }

    @Test
    public void emptyDequeHasNoMaximum() {
        MaxArrayDeque61B<Integer> mad =
                new MaxArrayDeque61B<Integer>(Comparator.naturalOrder());
        assertThat(mad.max()).isNull();
        assertThat(mad.max(Comparator.reverseOrder())).isNull();
    }

    @Test
    public void suppliedComparatorCanChooseADifferentMaximum() {
        MaxArrayDeque61B<Integer> mad =
                new MaxArrayDeque61B<Integer>(Comparator.naturalOrder());
        mad.addLast(3);
        mad.addLast(8);
        mad.addLast(5);

        assertThat(mad.max()).isEqualTo(8);
        // Reverse order considers the numerically smallest item the maximum.
        assertThat(mad.max(Comparator.reverseOrder())).isEqualTo(3);
        assertThat(mad.max()).isEqualTo(8); // The override does not change the default.
    }
}
