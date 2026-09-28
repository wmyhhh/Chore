import org.junit.platform.launcher.core.LauncherDiscoveryRequestBuilder;
import org.junit.platform.launcher.core.LauncherFactory;
import org.junit.platform.launcher.listeners.SummaryGeneratingListener;

import java.io.PrintWriter;
import java.util.Arrays;

import static org.junit.platform.engine.discovery.DiscoverySelectors.selectClass;

/** Runs selected deque tests without compiling the unfinished Project 1C parts. */
public class RunObjectMethodTests {
    public static void main(String[] args) {
        String[] classes = args.length == 0
                ? new String[]{"ArrayDeque61BTest", "LinkedListDeque61BTest", "Deque61BEqualityTest"}
                : args;

        var request = LauncherDiscoveryRequestBuilder.request()
                .selectors(Arrays.stream(classes).map(name -> selectClass(name)).toList())
                .build();
        var listener = new SummaryGeneratingListener();
        var launcher = LauncherFactory.create();
        launcher.registerTestExecutionListeners(listener);
        launcher.execute(request);

        var summary = listener.getSummary();
        summary.printTo(new PrintWriter(System.out));
        summary.getFailures().forEach(failure -> failure.getException().printStackTrace(System.out));
        if (summary.getTestsFoundCount() == 0 || summary.getTotalFailureCount() != 0) {
            System.exit(1);
        }
    }
}
