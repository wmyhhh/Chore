# Project 1C: Object methods 简单测试说明

课程 [Project 1C spec](https://sp24.datastructur.es/projects/proj1c/#testing-the-object-methods) 建议为 `ArrayDeque61B` 和 `LinkedListDeque61B` 分别编写 test class，检查 `iterator()`、`equals(Object)`、`toString()`。本仓库对应的文件是 [ArrayDeque61BTest.java](tests/ArrayDeque61BTest.java) 和 [LinkedListDeque61BTest.java](tests/LinkedListDeque61BTest.java)。`hashCode()` 虽然不属于 spec 指定的三个方法，但 override `equals` 后也应检查它们的 contract。

| 方法 | 最简单的 test case | 为什么要测 |
| --- | --- | --- |
| `iterator()` | 按顺序读完所有 item，再检查 `hasNext()` 为 `false`，`next()` 抛出 `NoSuchElementException` | 验证遍历顺序和结束行为；两个 test class 已有这些 tests |
| `equals(Object)` | 两个独立创建、内容顺序相同的 deque 相等；改变顺序后不相等 | 验证比较的是 logical sequence，而不是 object identity 或内部存储 |
| `hashCode()` | 相等的两个 deque 返回相同 hash code | 验证 `equals` 与 `hashCode` 的 Java contract；不同内容的 hash **允许碰撞**，不要断言一定不同 |
| `toString()` | 空 deque 为 `[]`；包含 `front`、`back` 时为 `[front, back]` | 验证输出反映从 front 到 back 的顺序 |

在 IntelliJ 中打开上述两个 test class，点击 class 左侧的绿色运行图标即可运行。额外的 [Deque61BEqualityTest.java](tests/Deque61BEqualityTest.java) 还检查了 array/linked 两种实现之间的对称相等性、`HashSet` 行为和其他边界情况。

如果项目后续的 `MaxArrayDeque61BTest` 因实现尚未完成而阻止 IntelliJ 编译整个 module，可以先在 Terminal 运行 `./proj1c/run-object-tests.sh`（从 `skeleton-sp24` 目录出发）。这只编译上述三个 test class 及其直接依赖；传入 `ArrayDeque61BTest` 或 `LinkedListDeque61BTest` 则只执行指定的 test class。这个脚本不会修改 `MaxArrayDeque61B`。

写 test 时要区分 `assertThat(deque).isEqualTo(otherDeque)` 与 `assertThat(deque).containsExactly(...)`：前者调用 deque 的 `equals(Object)`；后者利用 `Iterable<T>` 和 `iterator()` 逐项检查。`toString()` 需要显式调用后再比较 String。
