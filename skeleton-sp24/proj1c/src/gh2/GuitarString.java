package gh2;

import deque.ArrayDeque61B;
import deque.Deque61B;

/** Simulates a vibrating string with a fixed-length ring buffer of samples. */
public class GuitarString {
    /** Constants. Do not change. In case you're curious, the keyword final
     * means the values cannot be changed at runtime. We'll discuss this and
     * other topics in lecture on Friday. */
    private static final int SR = 44100;      // Sampling Rate
    private static final double DECAY = .996; // energy decay factor

    // The reference stays fixed; pluck() and tic() change its contents.
    // Public operations preserve the original logical size (at least two).
    private final Deque61B<Double> buffer;

    /* Create a guitar string of the given frequency.  */
    public GuitarString(double frequency) {
        if (!Double.isFinite(frequency) || frequency <= 0) {
            throw new IllegalArgumentException("frequency must be finite and positive");
        }
        // This is the number of samples, not the backing array's capacity.
        // Validate the long result before narrowing it to int to avoid overflow.
        long roundedSize = Math.round(SR / frequency);
        if (roundedSize < 2 || roundedSize > Integer.MAX_VALUE) {
            throw new IllegalArgumentException("frequency must produce 2 to Integer.MAX_VALUE samples");
        }
        int sampleCount = (int) roundedSize;
        buffer = new ArrayDeque61B<>();
        for (int i = 0; i < sampleCount; i++) {
            buffer.addLast(0.0);
        }
    }

    /* Pluck the guitar string by replacing the buffer with white noise. */
    public void pluck() {
        // Replace exactly the original number of samples. A for-each loop would
        // use an iterator while the deque is being structurally modified.
        int sampleCount = buffer.size();
        for (int i = 0; i < sampleCount; i++) {
            buffer.removeFirst();
            // Draw separately for each sample; keep the logical size unchanged.
            buffer.addLast(Math.random() - 0.5);
        }
    }

    /* Advance the simulation one time step by performing one iteration of
     * the Karplus-Strong algorithm.
     */
    public void tic() {
        double first = buffer.removeFirst();
        // After removal, the original second sample is now at the front.
        double second = buffer.get(0);
        double nextSample = (first + second) / 2 * DECAY;
        buffer.addLast(nextSample);
    }

    /* Return the double at the front of the buffer. */
    public double sample() {
        // Reading must not advance time; that is tic()'s responsibility.
        return buffer.get(0);
    }
}
