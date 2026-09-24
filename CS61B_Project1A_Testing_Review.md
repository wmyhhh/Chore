# CS 61B Project 1A Testing 复习笔记

> 主要参考：[CS 61B Project 1A — Writing Tests](https://sp24.datastructur.es/projects/proj1a/#writing-tests)、[Google Truth](https://truth.dev/)、[Truth `IterableSubject` API](https://truth.dev/api/latest/com/google/common/truth/IterableSubject.html) 与 [JUnit 5 `@Test` API](https://docs.junit.org/5.9.1/api/org.junit.jupiter.api/org/junit/jupiter/api/Test.html)。
>
> 本文关注 JUnit 5、Google Truth、assertion semantics、Arrange–Act–Assert、Test-Driven Development，以及如何测试 stateful data structure。Examples 用于说明 testing 思想，不是完整的 Project 1A test suite。

---

## 1. JUnit 与 Google Truth 的职责

```text
JUnit 5
├── 发现和运行 test methods
├── 提供 @Test annotation
├── 管理 test lifecycle
└── 汇总 success / failure

Google Truth
├── 编写 assertions
├── 比较 actual 与 expected
├── 为 List、String、boolean 等提供专用 assertions
└── 生成清晰的 failure messages
```

- **JUnit 5** 是 Testing Framework（测试框架）。
- **Google Truth** 是 Assertion Library（断言库）。
- Assertion 是一条可执行的声明：actual value 应满足某个 expected condition。
- Assertion 失败时通常抛出 `AssertionError`，JUnit 据此将 test 标记为 failed。
- Test method 正常结束且没有 uncaught exception 或 failed assertion 时，JUnit 将其标记为 passed。

---

## 2. 基本 Imports 与 `@Test`

```java
import org.junit.jupiter.api.Test;

import static com.google.common.truth.Truth.assertThat;
import static com.google.common.truth.Truth.assertWithMessage;
```

普通 import 让代码可以写 `@Test`，而不必写完整名称；static import 让代码可以直接调用 `assertThat(...)`，而不必写 `Truth.assertThat(...)`。

```java
@Test
public void emptyDequeHasSizeZero() {
    // test body
}
```

`@Test` 告诉 JUnit 这个 method 是 test method。JUnit 5 test method 不得是 `private` 或 `static`，且通常返回 `void`。Method name 不必以 `test` 开头，因为 `@Test` 已经完成标记。

---

## 3. Truth Assertion 的基本结构

```java
assertThat(actual).isEqualTo(expected);
```

例如：

```java
assertThat(deque.size()).isEqualTo(0);
```

含义是：

```text
actual   = deque.size()
expected = 0
```

Truth 的参数顺序是：

```java
assertThat(actual).isEqualTo(expected);
```

JUnit 原生 assertion 通常写成：

```java
assertEquals(expected, actual);
```

两者的 expected/actual 顺序不同，不要混淆。

### 3.1 `assertThat(actual)` 本身不执行检查

错误示例：

```java
assertThat(deque.isEmpty());
```

`assertThat(...)` 只是根据 actual type 创建一个 Truth `Subject`；如果没有调用 terminal assertion，test 不会检查任何 condition。

正确写法：

```java
assertThat(deque.isEmpty()).isTrue();
```

可以把 fluent chain 理解为：

```text
选择 actual value
        ↓
Truth 根据 type 创建 Subject
        ↓
terminal assertion 定义 expected condition
        ↓
满足则继续；不满足则抛 AssertionError
```

---

## 4. 常用 Truth Assertions

### 4.1 Equality

```java
assertThat(deque.size()).isEqualTo(3);
assertThat(deque.get(0)).isEqualTo("front");
assertThat(actual).isNotEqualTo(expected);
```

`isEqualTo()` 检查 logical equality。对于普通 objects，它主要依赖 `equals()` contract。

### 4.2 Boolean

```java
assertThat(deque.isEmpty()).isTrue();
assertThat(deque.isEmpty()).isFalse();
```

必须写 `.isTrue()` 或 `.isFalse()`；只写 `assertThat(booleanValue)` 不会检查结果。

### 4.3 `null`

```java
assertThat(deque.removeFirst()).isNull();
assertThat(deque.get(-1)).isNull();
assertThat(deque.get(0)).isNotNull();
```

### 4.4 Object Equality 与 Identity

```java
assertThat(actual).isEqualTo(expected);
assertThat(actual).isSameInstanceAs(expected);
assertThat(actual).isNotSameInstanceAs(expected);
```

- `isEqualTo()` 检查 logical equality。
- `isSameInstanceAs()` 检查两个 references 是否指向同一个 object，接近 `actual == expected`。
- Data-structure tests 通常关心 logical contents，不要求两个 collections 是同一个 instance。

### 4.5 Iterable / List

```java
assertThat(actualList).isEmpty();
assertThat(actualList).isNotEmpty();
assertThat(actualList).hasSize(3);
assertThat(actualList).contains("middle");
assertThat(actualList).doesNotContain("missing");
```

检查完整 contents 和 order：

```java
assertThat(actualList)
    .containsExactly("front", "middle", "back")
    .inOrder();
```

如果 expected 已经是 `List`：

```java
assertThat(actualList)
    .containsExactlyElementsIn(expectedList)
    .inOrder();
```

`containsExactly(...)` 检查没有缺少、多余 elements，并检查 duplicate counts；追加 `.inOrder()` 才进一步要求 iteration order 一致。

对 `List` 也可以使用：

```java
assertThat(actualList).isEqualTo(expectedList);
```

因为 `List.equals()` 本身考虑 elements 和 order；但 `containsExactlyElementsIn(...).inOrder()` 往往有更清楚的 intent 和 failure message。

---

## 5. `assertWithMessage`

```java
assertWithMessage("empty removal must not change size")
    .that(deque.size())
    .isEqualTo(0);
```

结构为：

```java
assertWithMessage(message)
    .that(actual)
    .terminalAssertion(expected);
```

好的 message 应提供 scenario context：

```text
empty removal must not change size
recursive lookup must preserve deque contents
size should increase after addLast
```

不要只重复 Truth 已经会报告的 actual 和 expected：

```text
expected 0 but got another value
```

---

## 6. Arrange–Act–Assert（AAA）

```java
@Test
public void removeFirstEmptyReturnsNull() {
    // Arrange
    Deque61B<String> deque = new LinkedListDeque61B<>();

    // Act
    String removed = deque.removeFirst();

    // Assert
    assertThat(removed).isNull();
    assertThat(deque.size()).isEqualTo(0);
    assertThat(deque.isEmpty()).isTrue();
    assertThat(deque.toList()).isEmpty();
}
```

### Arrange

建立 test 的 initial state，包括 instantiate object 和准备 elements。

### Act

执行真正想测试的 operation，最好保存 return value。

### Assert

验证：

1. Direct return value；
2. Resulting object state；
3. 通过 public API 可观察的 invariant。

一个 test 可以有多个 Act–Assert phases，但它们应属于同一个 coherent scenario，而不是把许多无关 behaviors 塞进同一 method。

---

## 7. Stateful Data Structure 的测试重点

普通 pure function 常表示为：

```text
input → output
```

Deque 是 Stateful Object（有状态对象），更接近：

```text
old state + operation
        ↓
return value + new state
```

所以不能只检查 return value。例如 query method 可能返回正确 element，却错误地修改 links。

### 7.1 验证 Query Method 不修改 State

```java
@Test
public void getRecursiveDoesNotModifyDeque() {
    Deque61B<Integer> deque = new LinkedListDeque61B<>();
    deque.addLast(10);
    deque.addLast(20);
    deque.addLast(30);

    List<Integer> before = deque.toList();

    int result = deque.getRecursive(1);

    assertThat(result).isEqualTo(20);
    assertThat(deque.toList())
        .containsExactlyElementsIn(before)
        .inOrder();
    assertThat(deque.size()).isEqualTo(3);
}
```

这里同时验证：

```text
Return-value postcondition
State-preservation postcondition
```

### 7.2 测试 Operation Sequence

一个 operation 可能留下 corrupted state，直到下一次 operation 才暴露，因此需要测试 method composition：

```java
@Test
public void removeFromBothEnds() {
    Deque61B<String> deque = new LinkedListDeque61B<>();
    deque.addLast("A");
    deque.addLast("B");

    String first = deque.removeFirst();
    assertThat(first).isEqualTo("A");
    assertThat(deque.toList()).containsExactly("B");

    String last = deque.removeLast();
    assertThat(last).isEqualTo("B");
    assertThat(deque.toList()).isEmpty();
    assertThat(deque.size()).isEqualTo(0);
    assertThat(deque.isEmpty()).isTrue();
}
```

---

## 8. Boundary Cases 与 Equivalence Classes

不必测试所有 integers，但要测试不同的 Equivalence Classes（等价类）。对于 indexed lookup：

```text
negative index
first valid index
middle valid index
last valid index
index == size
index much larger than size
```

```java
assertThat(deque.get(-1)).isNull();
assertThat(deque.get(0)).isEqualTo("A");
assertThat(deque.get(1)).isEqualTo("B");
assertThat(deque.get(2)).isNull();
assertThat(deque.get(1000)).isNull();
```

Data structure 常见 state classes：

```text
empty
singleton
multiple elements
singleton removal 后回到 empty
add after removal
mixed front/back operations
```

Boundary testing 的目标不是堆积 random examples，而是系统覆盖 semantic categories。

---

## 9. Test Oracle 与 Method Coupling

**Test Oracle（测试预言机）** 是判断 actual 是否正确的 expected source。

不推荐只写：

```java
assertThat(deque.getRecursive(1))
    .isEqualTo(deque.get(1));
```

如果两个 methods 有相同 bug，它们仍可能相等。更可靠的是使用明确 expected value，并额外检查 state：

```java
assertThat(deque.getRecursive(1)).isEqualTo(20);
assertThat(deque.toList())
    .containsExactly(10, 20, 30)
    .inOrder();
```

`toList()` 在被独立验证后可以作为 observation tool；在它尚未可靠时，应配合 debugger 或 Java Visualizer 检查 object graph，避免两个错误 methods 相互掩盖。

---

## 10. Black-Box Testing 与 Interface Type

推荐：

```java
Deque61B<String> deque = new LinkedListDeque61B<>();
```

普通 behavior tests 应使用 Black-Box Testing（黑盒测试）：

- 只调用 public API；
- 不访问 `sentinel`、`size` 或 `Node`；
- 不调用 private helper；
- 不依赖 implementation-specific representation；
- 根据 `Deque61B` contract 判断 correctness。

课程会将你的 test file 用于 staff implementation，因此 tests 应测试 interface behavior，而不是只适用于你的 private design。Staff 提供的 `PreconditionTest` 使用 reflection 检查 topology，属于特殊 White-Box Test（白盒测试），不代表普通 tests 也应读取 private fields。

---

## 11. Test Independence 与 Granularity

每个 test 应创建 fresh object：

```java
@Test
public void firstTest() {
    Deque61B<Integer> deque = new LinkedListDeque61B<>();
}

@Test
public void secondTest() {
    Deque61B<Integer> deque = new LinkedListDeque61B<>();
}
```

Test 应满足：

```text
可以单独运行
可以重复运行
不依赖其他 tests 留下的 state
不依赖 test execution order
```

JUnit 5 的默认 execution order 刻意不直观，unit tests 不应依赖顺序。

Test granularity 应以一个 coherent behavior/scenario 为单位：

- 太细：大量重复 Arrange code，阅读成本高；
- 太粗：第一个 assertion 失败后，许多无关 checks 不再执行；
- 合理：同一 state transition 或同一 contract 的多个 observations 放在一起。

---

## 12. Test Naming

推荐形式：

```text
method + condition + expected behavior
```

例如：

```java
removeFirstEmptyReturnsNull
removeSingletonMakesDequeEmpty
getNegativeIndexReturnsNull
getRecursiveDoesNotModifyDeque
sizeChangesAfterAddAndRemove
```

好名字能让 test report 直接说明哪个 contract 被破坏。JUnit 5 不要求 method name 包含 `test`；也可使用 `@DisplayName` 提供更自然的报告名称。

---

## 13. Coverage 不等于 Correctness

错误示例：

```java
@Test
public void noAssertionTest() {
    Deque61B<String> deque = new LinkedListDeque61B<>();
    deque.addFirst("A");
    deque.removeFirst();
}
```

它执行了 methods，却没有验证任何结果，因而很可能无条件通过。

只检查 return value 也可能不足：

```java
assertThat(deque.removeFirst()).isEqualTo("A");
```

更完整：

```java
String removed = deque.removeFirst();

assertThat(removed).isEqualTo("A");
assertThat(deque.toList()).isEmpty();
assertThat(deque.size()).isEqualTo(0);
assertThat(deque.isEmpty()).isTrue();
```

Coverage 只表示执行过哪些 code/scenarios，不证明 assertions 足够强，也不是 correctness proof。

---

## 14. Test-Driven Development（TDD）

```text
1. Red
   先写 test 并确认它失败

2. Green
   编写最少 implementation 使 test 通过

3. Refactor
   在 tests 保护下改善 naming、structure 和 duplication

4. Regression
   运行全部旧 tests，确认没有破坏已有 behavior
```

新 test 如果一开始就通过，需要判断：

- Implementation 是否已经正确；
- Test 是否真的被 `@Test` 标记并执行；
- 是否缺少 terminal assertion；
- Scenario 是否触发了目标 behavior；
- Expected value 是否写错；
- 是否依赖另一个具有相同 bug 的 method。

---

## 15. Java `assert`、Truth 与 JUnit Assertions

Java 语言本身有 built-in `assert` keyword：

```java
assert condition;
assert condition : message;
```

例如：

```java
assert size >= 0 : "size must not be negative";
```

Built-in assertions 通常默认 disabled，需要 JVM option `-ea` 才执行，所以不能替代 JUnit/Truth tests，也不适合检查 public API input。

| Syntax | 类型 | 是否默认执行 | 典型用途 |
|---|---|---:|---|
| `assert condition;` | Java keyword | 通常否，需要 `-ea` | 可选的内部 invariant check |
| `assertThat(actual).is...()` | Truth assertion | Test 运行时执行 | Project 1A 的主要 assertions |
| `assertEquals(expected, actual)` | JUnit assertion | Test 运行时执行 | JUnit 原生 equality assertion |

对于明确要求 exception 的 API，JUnit 还提供：

```java
assertThrows(
    IllegalArgumentException.class,
    () -> operation()
);
```

但 Project 1A 的 empty removal contract 是返回 `null`，不是抛 exception，因此不应使用 `assertThrows` 测试 empty removal。

---

## 16. Failure 后如何 Debug

Assertion failure 时按以下顺序处理：

1. 阅读 test name，确认 scenario；
2. 阅读 Truth message 中的 actual 与 expected；
3. 确认 expected 是否符合 interface contract；
4. 找到第一次失败的 Act–Assert phase；
5. 在该 operation 前设置 breakpoint；
6. 使用 Java Visualizer 检查 object graph；
7. 寻找 Representation Invariant 第一次失效的位置；
8. 修复后运行全部 regression tests，而不只运行当前 test。

不要根据 failure message 直接在出错行添加特殊分支。Test 显示的是 observable symptom，root cause 可能来自更早的 state mutation。

---

## 17. Project 1A Test Categories Checklist

### Initial state

- [ ] `isEmpty()` 为 `true`。
- [ ] `size()` 为 `0`。
- [ ] `toList()` 为空。

### Add operations

- [ ] Empty、singleton、multiple-element states。
- [ ] Repeated `addFirst()`。
- [ ] Repeated `addLast()`。
- [ ] Mixed front/back additions。
- [ ] 每次 operation 后验证 contents、size 和 emptiness。

### Iterative `get()`

- [ ] First、middle、last valid indices。
- [ ] Negative index。
- [ ] `index == size`。
- [ ] Very large index。
- [ ] Query 后 state 不变。

### Recursive `getRecursive()`

- [ ] 与 iterative `get()` 相同的 valid/invalid categories。
- [ ] 明确 expected value，而不是只与 `get()` 比较。
- [ ] Query 后 contents、size、emptiness 不变。

### Removal

- [ ] Empty removal 返回 `null` 且 state 不变。
- [ ] Singleton removal 返回 element 并进入 empty state。
- [ ] Multiple-element removal 返回正确 element。
- [ ] Repeated removal。
- [ ] `removeFirst()` 后 `removeLast()`。
- [ ] `removeLast()` 后 `removeFirst()`。
- [ ] Remove 后从相反一端 add。
- [ ] 同时验证 return value 与 resulting state。

### Test quality

- [ ] 每个 test 都有 terminal assertions。
- [ ] 每个 test 使用 fresh deque。
- [ ] Tests 不依赖 execution order。
- [ ] Tests 只使用 public API。
- [ ] Test names 描述 condition 和 expected behavior。
- [ ] 新 test 在 implementation 前应先观察到 Red。

---

## 18. Quick Reference

```java
// Equality
assertThat(actual).isEqualTo(expected);
assertThat(actual).isNotEqualTo(expected);

// Boolean
assertThat(condition).isTrue();
assertThat(condition).isFalse();

// null
assertThat(actual).isNull();
assertThat(actual).isNotNull();

// Identity
assertThat(actual).isSameInstanceAs(expected);
assertThat(actual).isNotSameInstanceAs(expected);

// Iterable / List
assertThat(actualList).isEmpty();
assertThat(actualList).hasSize(expectedSize);
assertThat(actualList).contains(expectedElement);
assertThat(actualList)
    .containsExactly(expectedElements)
    .inOrder();
assertThat(actualList)
    .containsExactlyElementsIn(expectedList)
    .inOrder();

// Custom failure context
assertWithMessage("scenario context")
    .that(actual)
    .isEqualTo(expected);
```

最终记忆：

```text
Test = Arrange + Act + Assert

Assertion = actual + expected condition

Stateful data-structure correctness
= return value correctness
+ resulting state correctness
+ invariant preservation
+ operation-sequence correctness

Coverage != Correctness
```
