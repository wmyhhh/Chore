/* Imports the required audio library from the
 * edu.princeton.cs.algs4 package. */
import edu.princeton.cs.algs4.StdAudio;
import org.junit.jupiter.api.Test;
import gh2.GuitarString;

import static com.google.common.truth.Truth.assertThat;
import static com.google.common.truth.Truth.assertWithMessage;
import static org.junit.jupiter.api.Assertions.assertThrows;

/** Tests the GuitarString class.
 *  @author Josh Hug
 */
public class TestGuitarString  {

    @Test
    public void testPluckTheAString() {
        double CONCERT_A = 440.0;
        GuitarString aString = new GuitarString(CONCERT_A);
        aString.pluck();
        for (int i = 0; i < 50000; i += 1) {
            StdAudio.play(aString.sample());
            aString.tic();
        }
    }

    @Test
    public void testSample() {
        GuitarString s = new GuitarString(100);
        assertThat(s.sample()).isEqualTo(0.0);
        assertThat(s.sample()).isEqualTo(0.0);
        assertThat(s.sample()).isEqualTo(0.0);
        s.pluck();

        double sample = s.sample();
        assertWithMessage("After plucking, your samples should not be 0").that(sample).isNotEqualTo(0);

        String errorMsg = "Sample should not change the state of your string";
        assertWithMessage(errorMsg).that(s.sample()).isWithin(0.0).of(sample);
        assertWithMessage(errorMsg).that(s.sample()).isWithin(0.0).of(sample);
    }

    @Test
    public void testTic() {
        GuitarString s = new GuitarString(100);
        assertThat(s.sample()).isEqualTo(0.0);
        assertThat(s.sample()).isEqualTo(0.0);
        assertThat(s.sample()).isEqualTo(0.0);
        s.pluck();

        double sample1 = s.sample();
        assertWithMessage("After plucking, your samples should not be 0").that(sample1).isNotEqualTo(0);

        s.tic();
        String errorMsg = "After tic(), your samples should not stay the same";
        assertWithMessage(errorMsg).that(s.sample()).isNotEqualTo(sample1);
    }

    @Test
    public void testTicCalculations() {
        // Create a GuitarString of frequency 11025, which
        // is a Deque61B of length 4.
        GuitarString s = new GuitarString(11025);
        s.pluck();

        // Record the front four values, ticcing as we go.
        double s1 = s.sample();
        s.tic();
        double s2 = s.sample();
        s.tic();
        double s3 = s.sample();
        s.tic();
        double s4 = s.sample();

        // If we tic once more, it should be equal to 0.996*0.5*(s1 + s2)
        s.tic();

        double s5 = s.sample();
        double expected = 0.996 * 0.5 * (s1 + s2);

        // Check that new sample is correct, using tolerance of 0.001.
        String errorMsg = "Wrong tic value. Try running the testTic method in TestGuitarString.java";
        assertWithMessage(errorMsg).that(s5).isWithin(0.001).of(expected);
    }

    @Test
    public void constructorRejectsUnusableFrequencies() {
        double[] invalid = {0.0, -100.0, Double.NaN, Double.POSITIVE_INFINITY,
            Double.NEGATIVE_INFINITY, 44100.0, 100000.0, Double.MIN_VALUE};
        for (double frequency : invalid) {
            assertThrows(IllegalArgumentException.class,
                    () -> new GuitarString(frequency), "frequency: " + frequency);
        }
    }

    @Test
    public void smallestRoundedBufferPreservesInitialSilence() {
        // 1.6 rounds to two samples, enough to read the second after removal.
        GuitarString s = new GuitarString(44100.0 / 1.6);
        for (int step = 0; step < 12; step++) {
            assertThat(s.sample()).isEqualTo(0.0);
            s.tic();
        }
    }

    @Test
    public void repeatedPlucksPreserveRoundedLengthAndUpdateSequence() {
        // 4.4 rounds to four samples, rather than rounding up to five.
        GuitarString s = new GuitarString(44100.0 / 4.4);
        for (int pluck = 0; pluck < 2; pluck++) {
            s.pluck();
            double[] original = new double[4];
            for (int i = 0; i < original.length; i++) {
                original[i] = s.sample();
                assertThat(original[i]).isAtLeast(-0.5);
                assertThat(original[i]).isLessThan(0.5);
                s.tic();
            }

            // After four tics, the buffer should contain [e, f, g, h].
            // The fourth update uses e, since the original first sample is gone.
            double e = 0.996 * 0.5 * (original[0] + original[1]);
            double[] expected = {e,
                0.996 * 0.5 * (original[1] + original[2]),
                0.996 * 0.5 * (original[2] + original[3]),
                0.996 * 0.5 * (original[3] + e)};
            for (double value : expected) {
                assertThat(s.sample()).isWithin(1e-12).of(value);
                assertThat(s.sample()).isWithin(1e-12).of(value);
                s.tic();
            }
        }
    }

}
