# CS 61B Project 1C：Java 与 Data Structure 知识梳理

> 对应版本：[CS 61B Spring 2024 — Project 1C: Deque61B Enhancements](https://sp24.datastructur.es/projects/proj1c/)。
>
> 本文整理开始 Project 1C 前需要掌握的概念，并在第 6 节详细解释 inner class、outer object、`private` access 与 iterator encapsulation。例子用于理解机制；其中可运行的 `InnerClassDemo` 是独立教学程序。
>
> 术语保留原始 English expressions；公式中的 `n` 表示有效元素个数，`C` 表示 backing array capacity。

## 目录

1. [Project 1C 的知识地图](#1-project-1c-的知识地图)
2. [Deque、ADT 与 representation invariant](#2-dequeadt-与-representation-invariant)
3. [Interface、static type 与 dynamic type](#3-interfacestatic-type-与-dynamic-type)
4. [Generics、wrapper types 与 type erasure](#4-genericswrapper-types-与-type-erasure)
5. [Iterable、Iterator 与遍历状态](#5-iterableiterator-与遍历状态)
6. [重点：inner class 为什么能访问 outer object 的 private fields](#6-重点inner-class-为什么能访问-outer-object-的-private-fields)
7. [Object methods：equals 与 toString](#7-object-methodsequals-与-tostring)
8. [Inheritance 与 composition](#8-inheritance-与-composition)
9. [Comparable、Comparator 与 maximum selection](#9-comparablecomparator-与-maximum-selection)
10. [GuitarString、ring buffer 与声音模拟](#10-guitarstringring-buffer-与声音模拟)
11. [测试策略与常见错误](#11-测试策略与常见错误)
12. [建议学习与实现顺序](#12-建议学习与实现顺序)
13. [自测问题](#13-自测问题)
14. [参考资料](#14-参考资料)

## 1. Project 1C 的知识地图

Project 1C 要为已有的 `LinkedListDeque61B`、`ArrayDeque61B` 添加 `iterator()`、`equals()`、`toString()`，实现 `MaxArrayDeque61B`，再完成 `GuitarString`。核心训练是让自定义 container 遵守通用 Java contract，并把它作为其他程序的组件。[项目说明](https://sp24.datastructur.es/projects/proj1c/)

| 项目部分 | Java 知识 | Data structure / algorithm 知识 |
|---|---|---|
| `iterator()` | `Iterable`、`Iterator`、inner class、enhanced for loop | logical order、traversal state、linear traversal |
| `equals()` | `Object`、overriding、`instanceof`、wildcard | sequence equality、representation independence |
| `toString()` | method overriding、textual representation | 按 logical order 展示内容 |
| `MaxArrayDeque61B` | inheritance、constructor、overloading、`Comparator` | linear scan、loop invariant |
| `GuitarString` | composition、`Double`、floating-point arithmetic | queue、ring buffer、state transition |

推荐的理解路径：

```text
同一个 Deque abstraction，两种内部表示
    → 用 interface 与 generics 表达共同操作
    → 用 iterator 统一访问元素
    → 定义内容相等与字符串表示
    → 用 Comparator 传入比较策略
    → 把 Deque 用作声音模拟的状态容器
```

## 2. Deque、ADT 与 representation invariant

### 2.1 Deque 是什么

**Deque = Double-Ended Queue**，通常读作 “deck”。它支持在 front 和 back 两端添加、删除元素。

```text
front ← [A, B, C] → back
```

典型操作有 `addFirst`、`addLast`、`removeFirst`、`removeLast`、`get`、`size`。Deque 可以按 **FIFO（First-In, First-Out）** 的方式使用，也可以按 **LIFO（Last-In, First-Out）** 的方式使用；具体行为取决于选择哪一端添加和删除。

### 2.2 ADT、API、interface 与 implementation

| 概念 | 完整名称或含义 | 在项目中的例子 |
|---|---|---|
| ADT | Abstract Data Type，描述操作及其抽象含义 | 支持两端添加、删除的 deque |
| API | Application Programming Interface，面向调用者的操作约定 | method signatures、返回值、边界行为 |
| Java interface | 用 Java type 表达操作约定 | `Deque61B<T>` |
| Implementation | 具体存储方式与算法 | linked nodes 或 circular array |

**Representation independence** 表示 client code 依赖可观察行为，而不是内部表示。逻辑上相同的 `[A, B, C]`，即使一个使用 nodes、另一个使用 array，也应该按同样的顺序遍历。

### 2.3 Linked deque 的 invariant

**Representation invariant** 是有效的数据结构状态始终应该满足的条件。使用 circular sentinel 的 **doubly linked list** 可以表示为：

```text
sentinel ⇄ A ⇄ B ⇄ C ⇄ sentinel
```

常见 invariant：

- 空 deque 中，`sentinel.next` 与 `sentinel.prev` 都指向 sentinel 自身。
- 相邻 nodes 的 `next`、`prev` 相互一致。
- `size` 等于真实元素个数，sentinel 不算元素。
- 从 `sentinel.next` 沿 `next` 前进，得到 front 到 back 的 logical order。

因此，iterator 最自然的状态是“下一次要访问的 node reference”。遇到 sentinel 说明结束，不能把 sentinel 当作普通元素返回。

### 2.4 Circular array 的 logical index 与 physical index

**Logical index** 是元素在 deque 中的位置；**physical index** 是元素在 backing array 中的实际下标。

```text
physical index:  0   1   2   3   4   5   6   7
array:          [C,  D,  _,  _,  _,  _,  A,  B]

logical order:  [A, B, C, D]
logical index:   0  1  2  3
```

若 `front` 表示第一个元素的 physical index，则有效 logical index `i` 的转换为：

```java
int physicalIndex = (front + i) % capacity;
```

若实现使用 `nextFirst` 表示第一个元素前面的空位，则转换为：

```java
int physicalIndex = (nextFirst + 1 + i) % capacity;
```

先确认 field 的语义，再写公式。遍历时不能直接从 backing array 的下标 `0` 开始输出，也不能把 unused slots 当成元素。

Java 的 `%` 是 remainder operator，负数参与时结果可能为负：

```java
-1 % 8;               // -1
Math.floorMod(-1, 8); // 7
```

向前移动 circular index 时，特别检查下标为 `0` 的情形。

### 2.5 复杂度，以及 amortized 的含义

| 操作 | Doubly linked deque | Circular array deque |
|---|---:|---:|
| 两端添加、删除 | O(1) | amortized O(1) |
| `get(i)` | 最坏 O(n) | O(1) |
| 合理实现的完整遍历 | O(n) | O(n) |
| 单次 resize | 不需要整体复制 | 通常 O(n) |

**Amortized analysis** 分析一串操作的总成本，再把成本分摊到每次操作。采用合理的 geometric resizing 策略时，array 偶尔发生 O(n) resize，仍可使两端操作具有 amortized O(1) 成本。它不等同于假设随机输入的 average-case analysis。

## 3. Interface、static type 与 dynamic type

```java
Deque61B<String> words = new ArrayDeque61B<>();
```

| 部分 | 含义 |
|---|---|
| `Deque61B<String>` | variable 的 declared type / static type |
| `words` | reference variable |
| `new ArrayDeque61B<>()` | instantiate 一个 object |
| `ArrayDeque61B` | object 的 runtime class / dynamic type |

**Compile time 根据 static type 检查哪些 methods 可调用；runtime 对被 override 的 instance method，根据实际 object 选择实现。** 后者称为 dynamic dispatch。

```java
Deque61B<String> words = new ArrayDeque61B<>();
words.addLast("hello");
```

Compiler 知道 `Deque61B` 提供 `addLast`；运行时调用实际 object 对应的实现。这是 **subtype polymorphism** 的基本用途。

如果 variable 的 static type 是 `Deque61B<String>`，即使实际 object 是 `MaxArrayDeque61B<String>`，也不能直接通过该 variable 调用 interface 未声明的 `max()`。

三种类型关系：

```java
class A implements SomeInterface { ... }
class B extends A { ... }
interface ChildInterface extends ParentInterface { ... }
```

分别是 class 实现 interface、class 继承 class、interface 扩展 interface。不要因为都涉及“复用”就混用 `extends` 与 `implements`。

## 4. Generics、wrapper types 与 type erasure

### 4.1 Type parameter 与 type argument

```java
class Container<T> {
    private T item;
}
```

`T` 是 **type parameter**；在 `Container<String>` 中，`String` 是 **type argument**。Generics 让同一份实现支持不同元素类型，并在 compile time 检查类型匹配。

```java
Deque61B<String> words = new ArrayDeque61B<>();
words.addLast("hello"); // 合法
// words.addLast(42);   // 编译错误
```

对于没有额外 type bound 的 `T`，compiler 不知道它是否支持数值运算、字符串方法或大小比较。因此不能随意对 `T` 写 `a > b`、`a + b` 或 `a.length()`。

### 4.2 Primitive、wrapper、boxing 与 unboxing

Java generic type argument 使用 reference type，因此写 `Deque61B<Double>`，不能写 `Deque61B<double>`。

| 术语 | 含义 |
|---|---|
| Primitive type | 例如 `int`、`double` |
| Wrapper class | 例如 `Integer`、`Double` |
| Autoboxing | 自动把 primitive value 转成对应 wrapper |
| Unboxing | 从 wrapper 取出 primitive value |

```java
samples.addLast(0.25);     // double → Double
double x = samples.get(0); // Double → double
```

如果 `get(0)` 返回 `null`，unboxing 会抛出 `NullPointerException`。数值计算前要确保 buffer 中存在合法 sample。

### 4.3 Type erasure 与 wildcard

**Type erasure** 表示 Java 编译时会擦除或替换 generic type 信息；通常不会为 `Deque61B<String>` 与 `Deque61B<Integer>` 生成两个独立 runtime classes。因此，对一个普通 `Object`，不能用 `instanceof Deque61B<String>` 检查它的元素类型。[Java Generics 文档](https://docs.oracle.com/javase/tutorial/java/generics/erasure.html)

可以使用：

```java
other instanceof Deque61B<?>
```

`?` 是 **unbounded wildcard**，表示元素类型未知。你可以把读取出的元素视为 `Object`，但不能向这个未知类型 container 随意添加非 `null` 的任意 object。

`Deque61B<?>` 也不同于 `Deque61B<Object>`：前者隐藏了某个具体类型，后者明确允许存放 `Object` 类型的值。Generic types 通常具有 **invariance**：`Deque61B<String>` 不是 `Deque61B<Object>` 的 subtype。

## 5. Iterable、Iterator 与遍历状态

### 5.1 Container 与一次遍历的区别

| Interface | 责任 | 核心 method |
|---|---|---|
| `Iterable<T>` | 提供遍历器 | `Iterator<T> iterator()` |
| `Iterator<T>` | 保存一次遍历的进度 | `boolean hasNext()`、`T next()` |

可以把 container 看作一本书，把 iterator 看作某位阅读者的书签。多位阅读者共享同一本书，但书签位置各自独立。

**Enhanced for loop**：

```java
for (String word : words) {
    System.out.println(word);
}
```

对于 `Iterable` object，在概念上等价于：

```java
Iterator<String> it = words.iterator();
while (it.hasNext()) {
    String word = it.next();
    System.out.println(word);
}
```

Array 也支持 enhanced for，但那是语言另外规定的情况，不能据此认为 array 实现了 `Iterable`。[Java Iterable 文档](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Iterable.html)

### 5.2 两个 method 的行为

- `hasNext()` 只检查是否还有元素，不推进进度。
- `next()` 返回下一个元素，并推进进度。
- 根据标准 Java contract，耗尽后调用 `next()` 应抛出 `NoSuchElementException`。
- `Iterator.remove()` 是 optional operation；不实现时可以使用 interface 的默认行为，抛出 `UnsupportedOperationException`。[Java Iterator 文档](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Iterator.html)

```text
deque = [A, B]

hasNext() → true
hasNext() → true
next()    → A
hasNext() → true
next()    → B
hasNext() → false
```

Iterator 推进自己的 cursor，不应该通过删除 deque 元素完成普通遍历。

### 5.3 每个 iterator 都要有自己的 state

```java
Iterator<String> first = words.iterator();
Iterator<String> second = words.iterator();
```

推进 `first` 不应该推进 `second`。因此不要让所有 iterator 共用 deque field 中的一个 traversal cursor，也不要让 `iterator()` 永远返回同一个已经走到中途的 iterator。

这对 nested loops 尤其重要：外层和内层各自需要独立的遍历进度。

### 5.4 底层结构决定 iterator 的内部算法

Linked deque iterator 适合保存 node reference，每次前进一条 link。若每次 `next()` 都调用 `get(i)`，完整遍历可能累积为 `1 + 2 + ... + n`，即 O(n²)。

Array deque iterator 可以保存 logical index，再转换为 physical index；每一步 O(1)，完整遍历 O(n)。无论哪种实现，都应该遍历有效元素，并保持 front 到 back 的顺序。

## 6. 重点：inner class 为什么能访问 outer object 的 private fields

### 6.1 先把原句拆成三个问题

“非 `static` inner class 可以访问所属 outer object 的 `private` instance fields”实际包含三个独立问题：

1. **访问权限**：为什么 nested class 内的代码能够访问 `private` member？
2. **Object 关联**：如果创建了两个 outer objects，inner object 到底访问哪一个？
3. **封装边界**：iterator 能访问内部字段，为什么 client 仍不能直接访问它们？

其中 `private` 决定哪些代码位置有权限；object reference 决定访问哪一个 instance。必须把这两个维度分开。

### 6.2 Outer class、outer object 与 inner object

```java
class Outer {
    private int size;

    class Cursor {
        int readSize() {
            return size;
        }
    }
}
```

| 表达式或术语 | 含义 |
|---|---|
| `Outer` | outer / enclosing class，是 class declaration |
| `new Outer()` | 一个 outer object，也叫 enclosing instance |
| `Cursor` | 非 `static` member inner class |
| `outer.new Cursor()` | 创建与指定 outer object 关联的 inner object |

本文重点讨论这种 **non-static member inner class**。Java 还有 local class、anonymous class 等形式，不需要在开始本项目时一次掌握所有变体。

**一个 outer object 可以关联多个 inner objects。每个 inner object 是独立 object，有自己的 fields，同时关联着创建它时确定的 enclosing instance。** 这里的“属于”不是继承，也不意味着两个 objects 是同一个 object。[JLS §8.1.3](https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html#jls-8.1.3)

### 6.3 为什么能访问 private：lexical access rule

**Lexical nesting** 指 source code 中 class declaration 的嵌套关系。Java 的 `private` 访问规则允许同一 enclosing top-level class 内的相关嵌套代码访问其 private members。把 `private` 理解成“只能由当前 object 的 methods 访问”并不准确。[JLS §6.6.1](https://docs.oracle.com/javase/specs/jls/se17/html/jls-6.html#jls-6.6.1)

例如：

```java
class Outer {
    private int size = 3;

    private class Cursor {
        int readSize() {
            return size; // 合法：处于允许访问的 lexical scope
        }
    }
}
```

这里不需要把 `size` 改成 `public`，也不需要专门提供一个暴露内部状态的 getter。Iterator 是 container 内部 implementation 的一部分，可以直接使用这些细节。

反过来，一个独立 top-level client class，即使在同一个 package、甚至同一个 `.java` 文件里，也不会仅因为位置相近就获得访问 private fields 的权限。

### 6.4 为什么知道访问哪个 object：enclosing instance

考虑两个外部 objects：

```java
Outer a = new Outer();
Outer b = new Outer();

Outer.Cursor ca = a.new Cursor();
Outer.Cursor cb = b.new Cursor();
```

这段示意假定 `Cursor` 对调用位置可见。`ca` 关联 `a`，`cb` 关联 `b`。在实际项目中通常把 iterator class 设为 `private`，client 就不会直接使用这套创建语法。

```text
ca ── enclosing instance ──→ a
cb ── enclosing instance ──→ b
```

在 `Outer` 的 instance method 中写 `new Cursor()`，会把当前的 `Outer.this` 作为 enclosing instance。这正是 deque 的 `iterator()` 能自然创建“遍历当前 deque 的 iterator”的原因。

为了理解，可以把它近似想象为 iterator 额外保存了一个 `owner` reference；这是 conceptual model，不必依赖 compiler 生成的具体 field 名称或底层布局。

**Inner object 没有复制 outer fields。** 它访问的是相应 outer object 中的状态。

### 6.5 完整可运行例子：private array、独立 cursor 和 public interface

下面是独立教学程序。保存为 `InnerClassDemo.java` 后可以编译运行。`WordSequence` 只保存三个字符串，便于把注意力集中在 Java 机制上。

```java
import java.util.Iterator;
import java.util.NoSuchElementException;

class WordSequence implements Iterable<String> {
    private final String[] items = {"A", "B", "C"};
    private final int size = items.length;

    public void replaceFirst(String value) {
        items[0] = value;
    }

    @Override
    public Iterator<String> iterator() {
        return new WordIterator();
    }

    private class WordIterator implements Iterator<String> {
        private int cursor = 0;

        @Override
        public boolean hasNext() {
            return cursor < WordSequence.this.size;
        }

        @Override
        public String next() {
            if (!hasNext()) {
                throw new NoSuchElementException();
            }
            String result = WordSequence.this.items[cursor];
            cursor += 1;
            return result;
        }
    }
}

public class InnerClassDemo {
    public static void main(String[] args) {
        WordSequence words = new WordSequence();
        Iterator<String> first = words.iterator();
        Iterator<String> second = words.iterator();

        System.out.println(first.next());  // A
        System.out.println(first.next());  // B
        System.out.println(second.next()); // A

        Iterator<String> live = words.iterator();
        words.replaceFirst("X");
        System.out.println(live.next()); // X

        WordSequence other = new WordSequence();
        System.out.println(other.iterator().next()); // A

        for (String word : words) {
            System.out.println(word); // X, B, C，各占一行
        }
    }
}
```

预期输出：

```text
A
B
A
X
A
X
B
C
```

这里 `private final String[] items` 的 `final` 表示不能给 `items` 重新赋另一个 array reference，不代表 array contents 不可修改。因此 `items[0] = value` 合法。

### 6.6 逐步解释 object 与 state

执行 `words.iterator()` 时，会 instantiate 一个新的 `WordIterator`。连续调用两次，就得到两个 iterator objects：

```text
first  ──→ WordIterator object #1
            cursor = 0
            enclosing instance ──┐
                                 ↓
                            words object
                            items = [A, B, C]
                            size = 3
                                 ↑
second ──→ WordIterator object #2 │
            cursor = 0           │
            enclosing instance ──┘
```

第一次 `first.next()` 读取 `words.items[0]`，然后把 #1 的 `cursor` 改成 `1`。第二次把 #1 的 `cursor` 改成 `2`。#2 的 `cursor` 仍为 `0`，所以 `second.next()` 返回 `A`。

这体现了 **shared container state + independent traversal state**：底层数据共享，遍历进度独立。

`live` 创建后，通过 `replaceFirst` 修改 `words.items[0]`，它随后读到 `X`。这说明本例 iterator 直接访问原 array，而不是在创建时复制 snapshot。这里明确设计了“读取当前 array 内容”的行为；不能因此推断所有 Java iterators 都允许任意修改 container。

对通用 Java iterator，遍历过程中修改 container 的行为取决于具体实现的 policy。**Fail-fast iterator** 会检测某些 structural modifications 并报错，但创建 inner class 不会自动获得这种能力。

### 6.7 `this` 和 `OuterClass.this` 分别指谁

在 `WordIterator` 的 instance method 中：

```java
this                       // 当前 WordIterator object
this.cursor                // 当前 iterator 的 cursor
WordSequence.this          // 与它关联的 WordSequence object
WordSequence.this.items    // 该 sequence 的 private array
```

如果没有同名 variable 发生遮蔽，`items` 通常就可以直接写，不必每次写完整限定形式。示例显式写 `WordSequence.this.items` 是为了让 object 关系更清楚。

**Shadowing** 是内层 declaration 遮蔽外层同名 declaration。例如：

```java
class ShadowExample {
    private int value = 10;

    class Inner {
        private int value = 20;

        void show(int value) {
            System.out.println(value);                   // parameter
            System.out.println(this.value);              // Inner field
            System.out.println(ShadowExample.this.value); // Outer field
        }
    }
}
```

若传入 `30`，依次输出 `30`、`20`、`10`。`OuterClass.this` 是取得 enclosing instance 的 **qualified this** 表达式，不是 cast，也不是 superclass reference。[Oracle Nested Classes 教程](https://docs.oracle.com/javase/tutorial/java/javaOO/nested.html)

### 6.8 为什么没有把 backing array 暴露给 client

看 `iterator()` 的 signature：

```java
public Iterator<String> iterator() {
    return new WordIterator();
}
```

它有两个 type 层次：

- 返回值声明的 type 是公开的 `Iterator<String>`。
- 实际 object 的 class 是私有的 `WordIterator`。

Client 通过 interface 调用 `hasNext()`、`next()`，无需知道实际 class 的名字。`WordIterator` 的 methods 是 `public`，因为它们实现 interface 中的 public methods；iterator class 本身仍可以是 `private`。

下面这些从独立 client class 发起的访问不合法：

```java
// words.items;                   // items 是 private
// words.size;                    // size 是 private
// WordSequence.WordIterator it;  // WordIterator 是 private
// first.cursor;                  // Iterator interface 不提供 cursor
```

执行 `first.next()` 时，真正访问 `items` 的代码位于 `WordIterator.next()` 的 method body 内。这段代码本来就在允许访问的 lexical scope 中；不会因为是外部 client 调用它，就失去这种权限。反过来，client 也不会因为调用成功就继承这种权限。

因此，权限流不是“client 获得 array 的访问权”，而是“client 请求内部对象执行一个受控操作”。这就是 **encapsulation**：implementation 知道细节，client 使用 contract。

例如，若直接返回原始 backing array：

```java
public String[] exposeItems() {
    return items;
}
```

Client 就能随意修改 array slots，这叫 **representation exposure**，可能破坏 container 的 invariant。标准 iterator interface 不提供这种原始存储访问。

但“内部结构不暴露”不等于“所有内容都是 immutable”。Iterator 通常返回元素本身的 reference；如果元素是 mutable object，client 仍可能修改元素的内容。这里保护的是 container 的内部结构，是否复制元素是另一个设计问题。

### 6.9 与 static nested class 的真正区别

**Static nested class 不会自动关联某一个 outer object，但它仍具有相应的 private access 权限。** 如果显式传入 outer object reference，就可以访问那个 object 的 private fields。

```java
class Vault {
    private int amount = 7;

    static class Reader {
        private final Vault owner;

        Reader(Vault owner) {
            this.owner = owner;
        }

        int read() {
            return owner.amount; // 合法：显式 reference + private access
        }
    }
}
```

使用方式：

```java
Vault vault = new Vault();
Vault.Reader reader = new Vault.Reader(vault);
System.out.println(reader.read()); // 7
```

如果在 `Reader.read()` 中直接写 `return amount;`，会出错，因为没有隐式 enclosing `Vault` instance 可供解析这个 instance field。问题在于缺少接收对象，不在于 `amount` 是 private。

| 维度 | Non-static member inner class | Static nested class |
|---|---|---|
| 隐式 enclosing instance | 有 | 没有 |
| 直接使用 outer instance field 的简单名称 | 未被遮蔽且上下文允许时可以 | 不可以，需要明确 object reference |
| 通过 outer reference 访问其 private field | 可以 | 也可以 |
| outer 的 type parameter `T` | 可在相关 instance context 中使用 | 不能直接借用，需要自己的 type parameter 等设计 |
| 常见创建方式 | outer instance method 内 `new Inner()` | `new Outer.Nested(...)` |
| 自动成为 outer 的 subclass | 不会 | 不会 |

所以，项目常用 inner iterator 是因为“自动关联当前 deque + 能直接访问其内部状态”很方便，并不意味着 static nested iterator 无法实现同样功能。[JLS §8.1.3](https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html#jls-8.1.3)、[JLS §6.6.1](https://docs.oracle.com/javase/specs/jls/se17/html/jls-6.html#jls-6.6.1)

### 6.10 回到 generic Deque 与 Node

在一个 generic linked deque 中，可以看到这样的声明形状：

```java
class LinkedExample<T> implements Iterable<T> {
    private Node sentinel;

    private class Node {
        T item;
        Node next;
        Node prev;
    }

    private class LinkedIterator implements Iterator<T> {
        private Node current;

        // hasNext()、next() 的实现省略
    }

    // iterator() 和其他操作省略
}
```

这是结构示意，省略了必要的 interface methods，不能单独编译。需要理解：

- `Node` 和 `LinkedIterator` 都在 `LinkedExample<T>` 内部。
- 它们可以在相关 instance context 使用 outer 的 `T`，通常不需要再次声明 `<T>`。
- `current` 属于每个 iterator；`sentinel` 属于 deque。
- `next()` 返回 `current.item`，随后推进 node reference，client 不需要知道 `Node`。
- 把 iterator 声明为 `class LinkedIterator<T>` 会引入新的 type parameter，并遮蔽 outer 的 `T`，通常不是这里想要的设计。

开始实现前，试着自己回答：**谁拥有元素？谁拥有 cursor？`this` 指谁？谁有权限看 sentinel？client 得到的是 Node 还是 T？** 能回答这五个问题，inner iterator 的结构就清楚了。

## 7. Object methods：equals 与 toString

### 7.1 Identity 与 logical equality

```java
String a = new String("hello");
String b = new String("hello");

System.out.println(a == b);      // false
System.out.println(a.equals(b)); // true
```

对 reference，`==` 检查 **reference identity**，即是否指向同一个 object；`equals()` 检查 class 定义的 **logical equality**。`Object` 默认实现使用 identity，因此 container 若要按内容比较，需要 override。

Deque 的 **sequence equality** 可以表述为：长度相同，并且每个对应位置的元素相等。

```text
[A, B, C] 与 [A, B, C] → 相等
[A, B, C] 与 [C, B, A] → 不相等
[A, B]    与 [A, B, B] → 不相等
```

Capacity、physical index、node identity 都不是 sequence equality 的一部分。两种 Deque implementation 也可以表示相同 sequence。

### 7.2 Overriding 与 overloading

```java
@Override
public boolean equals(Object other) {
    // ...
}
```

这是正确 override `Object.equals` 的 signature。若改成 `equals(Deque61B<T> other)`，就声明了 parameter type 不同的新 method，属于 **overloading**，没有 override `equals(Object)`。

`@Override` 会要求 compiler 检查你是否真的在 override；因此它能及时暴露这种错误。

### 7.3 类型检查、null 与比较流程

现代 Java 的 **pattern matching for instanceof** 可以同时检查类型并提供已匹配的 variable：

```java
if (other instanceof Deque61B<?> otherDeque) {
    // 可以使用 otherDeque
}
```

这里 `other == null` 时不会匹配成功。对 pattern variable 的访问范围由 compiler 根据控制流判断。[Java Pattern Matching 文档](https://docs.oracle.com/en/java/javase/17/language/pattern-matching-instanceof.html)

实现 sequence equality 时可以依次考虑 identity、是否为合适的 deque type、size 是否相同，最后按顺序比较元素。使用两个 O(1)-per-step iterators 可以避免 linked deque 中重复 `get(i)` 带来的 O(n²) 遍历成本；总成本还要计入元素自身的 `equals()` 成本。

如果 container 的 contract 允许 `null` 元素，`Objects.equals(a, b)` 可以安全处理 null。不要用元素的 `==` 替代它们自己的 equality。

### 7.4 equals contract 与 hashCode

| 性质 | 含义 |
|---|---|
| Reflexivity | `x.equals(x)` 为 true |
| Symmetry | `x.equals(y)` 与 `y.equals(x)` 结果一致 |
| Transitivity | x 等于 y、y 等于 z，则 x 等于 z |
| Consistency | 相关状态不变时，反复比较结果一致 |
| Null rule | 非空 x 的 `x.equals(null)` 为 false |

相等 objects 必须具有相同 `hashCode()`；不同 objects 允许具有相同 hash code。通用 Java class override `equals` 时应同时维持这一 contract，这是后续学习 hash-based containers 的基础。本项目列出的任务与这条通用 Java 设计责任应分别理解。[Java Object 文档](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Object.html)

### 7.5 toString 的责任

`toString()` 给出便于阅读的 textual representation，例如 `[]`、`[A]`、`[A, B, C]`。它应保持 logical order，且不修改 container。

不能用 `toString()` 相同来判定 objects 相等。默认 object 显示中的 `@` 后面是 hash code 的十六进制形式，不能可靠地当作内存地址。

手动构建长字符串时可以使用 `StringBuilder`，避免循环中反复复制已有字符串。若直接复用已有 sequence 的字符串格式，则需确认项目允许相关 helper method。

## 8. Inheritance 与 composition

### 8.1 MaxArrayDeque61B 的 inheritance

```java
class MaxArrayDeque61B<T> extends ArrayDeque61B<T> {
    // 添加比较规则与 maximum selection
}
```

这里是 **is-a relationship**：MaxArrayDeque61B 具有普通 array deque 的操作，并添加新能力。已有存储与添加删除逻辑应通过 inheritance 复用。

Constructor 不会被继承。Subclass constructor 需要完成 superclass initialization；若没有显式调用其他 constructor，通常会隐式调用 `super()`，因此 superclass 必须存在可访问的无参数 constructor。

Subclass 不能直接访问 superclass 的 private fields，可以通过可访问的 methods 使用既有能力。不要把“inner class 能访问 private outer field”和“subclass 能访问 private superclass field”混为一谈：lexical nesting 与 inheritance 是不同关系。[Java Inheritance 文档](https://docs.oracle.com/javase/tutorial/java/IandI/subclasses.html)

### 8.2 GuitarString 的 composition

```java
class GuitarString {
    private Deque61B<Double> buffer;
}
```

这里是 **has-a relationship**：GuitarString 持有 deque 作为组件。它依赖 deque 的 API，而不需要读取 node 或 backing array。

使用 interface type 声明 field，使具体 implementation 可以替换，同时保留调用者依赖的操作约定。

## 9. Comparable、Comparator 与 maximum selection

### 9.1 谁定义“大于”

对字符串，“最大”可以表示 lexicographic order 最大、length 最长，或者自定义评分最高。Generic container 无法替 client 决定。

| Interface | 规则位置 | 调用方式 |
|---|---|---|
| `Comparable<T>` | 元素 class 自身的 natural ordering | `a.compareTo(b)` |
| `Comparator<T>` | 外部比较器 object | `comparator.compare(a, b)` |

`Comparable` 适合表达 class 的自然顺序，`Comparator` 则让同一组 objects 使用不同规则。[Java Comparable 文档](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Comparable.html)

### 9.2 Comparator 的 contract

```java
class LengthComparator implements Comparator<String> {
    @Override
    public int compare(String a, String b) {
        return Integer.compare(a.length(), b.length());
    }
}
```

返回负数表示第一个参数更小，零表示在此规则下等价，正数表示更大。只保证符号，不保证具体返回 `-1`、`0`、`1`。判断更大应使用 `> 0`。

```java
Comparator<String> byLength = new LengthComparator();
byLength.compare("cat", "elephant"); // 负数
byLength.compare("cat", "dog");      // 0
```

`"cat"` 和 `"dog"` 在长度规则下等价，不代表它们的 `equals()` 为 true。Comparator 应满足方向一致和 transitivity 等性质。[Java Comparator 文档](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Comparator.html)

对于整数，优先使用 `Integer.compare(a, b)`，而不是 `a - b`；后者可能发生 integer overflow，改变结果符号。

### 9.3 Lambda expression

熟悉普通 class 写法后，可以认识等价的 lambda expression：

```java
Comparator<String> byLength =
        (a, b) -> Integer.compare(a.length(), b.length());
```

Comparator 是 **functional interface**，可以用 lambda 提供其核心 comparison behavior。也可以用 `Comparator.naturalOrder()` 得到遵循元素自然顺序的 comparator。

### 9.4 Linear scan 与 loop invariant

找 maximum 的直接算法：以第一个有效元素作为 candidate，依次比较其余元素，遇到更大的就替换 candidate。

**Loop invariant**：处理完前 k 个元素后，candidate 是这 k 个元素中按照给定 comparator 的最大值。

不要把 candidate 初始化成 `0`：输入可能全为负数，也可能根本不是数值类型。若单次 comparison 为 O(1)，完整扫描为 O(n) time、O(1) extra space；无需先排序。

### 9.5 默认规则与本次调用规则

项目提供 `max()` 与 `max(Comparator<T> c)`：前者使用 constructor 保存的规则，后者使用本次传入的规则。空 deque 返回 `null`，并列最大可以返回其中任意一个。[MaxArrayDeque61B 要求](https://sp24.datastructur.es/projects/proj1c/#maxarraydeque61b)

这两个 methods 是 overloading。设计上可以让无参数版本复用有参数版本的扫描逻辑，避免写两份相同算法。

临时规则不应该意外替换默认规则。这个设计体现 **Strategy Pattern**：流程保持稳定，把可替换的比较策略作为 object 传入。

## 10. GuitarString、ring buffer 与声音模拟

### 10.1 Sample 与 sample rate

**Digital Signal Processing（DSP）** 中，声音可以表示为按时间排列的 samples：`x[0], x[1], x[2], ...`。Sample 是振幅值，**sample rate** `fs` 表示每秒处理多少个 sample，相邻 samples 的时间间隔是 `1 / fs`。

长度为 `N` 的 ring buffer 产生约 `N / fs` 的循环延迟。因此 fundamental frequency 可粗略理解为 `f ≈ fs / N`：buffer 越长，音高通常越低。Averaging filter 也会影响实际频率，因此这是近似关系。[Princeton Guitar String 说明](https://introcs.cs.princeton.edu/java/assignments/guitar.html)

### 10.2 Buffer length 不等于 capacity

**Buffer length** 是算法保存的有效 sample 数量；**array capacity** 是底层 array 的槽位数。例如 buffer 可以有 100 个 samples，而 array capacity 为 128。决定上述循环延迟的是有效 sample 数量。

Ring buffer 描述循环反馈的使用方式；底层可以使用 linked deque，也可以使用 circular array deque。

### 10.3 Karplus–Strong 的一次 state transition

令前两个 samples 为 `a`、`b`，decay factor 为 `d`。新 sample 为：

```text
newSample = d × (a + b) / 2
```

例如取 `d = 0.996`：

```text
更新前：[0.3, -0.1, 0.2, -0.4]

newSample = 0.996 × (0.3 + (-0.1)) / 2
          = 0.0996

更新后：[-0.1, 0.2, -0.4, 0.0996]
```

操作顺序是：移除并保存原 front，读取新的 front，计算新 sample，把它添加到 back。一次完整更新前后，buffer length 不变。这一更新要求至少有两个 samples；初始化时需遵守 skeleton 对频率和长度的约定。

Averaging 起到 **low-pass filter** 的作用，逐渐削弱较高频成分；decay 模拟振动衰减。随机 noise 提供初始激励，随后由反馈循环持续演化。[Karplus–Strong 原理说明](https://introcs.cs.princeton.edu/java/assignments/guitar.html)

### 10.4 Observer、mutator 与播放职责

| 操作 | 责任 |
|---|---|
| Constructor | 建立固定长度、初值为零的 sample buffer |
| `pluck()` | 用随机 noise 替换 samples，保持有效长度 |
| `sample()` | 读取当前 sample，不推进模拟 |
| `tic()` | 推进一次 state transition |
| Client 播放逻辑 | 把 sample 交给音频输出 |

`sample()` 是 **observer**，`tic()` 是 **mutator**。读状态与修改状态分开，便于精确控制和测试。

如果用 `Math.random() - 0.5` 产生 noise，其范围是 `[-0.5, 0.5)`。替换 samples 时不能只追加新值，否则 buffer length 会增加。

### 10.5 Array 与 linked implementation 的取舍

两者都能有效支持 front removal、front access、back insertion。Array 通常具有较好的 locality，也减少了 node allocation；linked implementation 通常会在持续添加时创建新 node。使用 `Double` 的 generic container 还涉及 boxing，不能把 array version 理解成完全没有 object allocation。

## 11. 测试策略与常见错误

### 11.1 测试矩阵

| 对象 | 应覆盖的情况 |
|---|---|
| Iterator | 空、单元素、多元素、wrap-around、两个 iterator、nested loops |
| `hasNext()` | 连续调用多次不改变下次返回值 |
| `next()` | 顺序正确，不删除数据，耗尽行为符合 contract |
| `equals()` | 同内容、不同顺序、不同长度、跨 implementation、null、无关类型 |
| `toString()` | 空结构、逗号和空格、logical order、不改变数据 |
| `max()` | 空、单元素、全负数、并列最大、不同 comparator、默认规则保留 |
| `GuitarString` | 零初始化、确定状态下的一次更新、长度不变、读取不推进 |

### 11.2 Truth 中内容与顺序要分开检查

```java
assertThat(actual).containsExactly("A", "B", "C");
```

这检查元素及重复次数，默认不要求顺序。要检查 sequence order：

```java
assertThat(actual)
        .containsExactly("A", "B", "C")
        .inOrder();
```

否则打乱顺序的 iterator 也可能通过测试。[Truth IterableSubject 文档](https://truth.dev/api/latest/com/google/common/truth/IterableSubject.html)

### 11.3 Floating-point 与随机行为

Floating-point 计算通常使用 tolerance：

```java
assertThat(actual).isWithin(1e-9).of(expected);
```

随机 `pluck()` 不应该断言具体随机序列；适合检查 sample 范围、有效长度等性质。`tic()` 则应尽量从已知初始 samples 出发，手算期望结果。

### 11.4 常见错误定位

| 错误 | 可能原因 |
|---|---|
| 每调用一次 `hasNext()` 就跳过元素 | 检查 method 错误地推进 cursor |
| 两个 iterator 相互干扰 | cursor 存在 deque 中，或共享同一个 iterator object |
| Array 遍历顺序不对 | 把 physical order 当成 logical order |
| Linked 遍历明显变慢 | 每一步反复调用 `get(i)` |
| `equals` 看似正确但测试失败 | parameter 写成具体 deque type，形成 overloading |
| 两个字符串内容相同却比较不等 | 对元素使用 `==` |
| 泛型 maximum 无法编译 | 对 `T` 使用 `>`，没有借助 comparator |
| Inner class 的 `this.size` 无法解析 | `this` 是 iterator，size 属于 outer object |
| Static nested class 无法直接读取 outer field | 缺少明确的 outer object reference |
| `sample()` 调用后声音状态改变 | observer 混入了 mutator 的职责 |

## 12. 建议学习与实现顺序

1. **复查 1A、1B invariant**：画出空 linked deque、wrapped array，以及元素的 logical order。
2. **掌握 interface 与 generics**：解释 static type、dynamic type、type parameter 与 wrapper。
3. **先理解独立教学 iterator**：运行第 6 节例子，逐步追踪 outer fields 与每个 cursor。
4. **实现两种 deque 的 iterator**：先验证顺序，再验证 iterator 独立性和边界行为。
5. **实现 object methods**：按 sequence semantics 思考 equality 与 display。
6. **练习不同 Comparators**：再把 maximum scan 添加到继承已有 array deque 的 class 中。
7. **手算 GuitarString 更新**：确认 sample、tic、pluck 各自职责后实现。
8. **做针对性验证**：优先覆盖 wrap-around、跨实现 equality、规则切换和 buffer length。

项目约束：`iterator()`、`equals()` 不允许调用 `toList()`；复制旧代码时保留 `package deque;`；不要在 `GuitarString` 内调用 `StdAudio.play`，播放由 client 负责。[项目实现要求](https://sp24.datastructur.es/projects/proj1c/)

`package deque;` 声明 class 所属 namespace；其他 package 可通过 `import deque.ArrayDeque61B;` 等方式引用可见的 class。Import 使名字可用，不会 instantiate object，也不会绕过 access control。

## 13. 自测问题

建议先遮住右栏，尝试用自己的语言解释。

| 问题 | 回答要点 |
|---|---|
| Deque 与 circular array 是同一层次的概念吗？ | Deque 是抽象行为，circular array 是一种表示方式。 |
| `Iterable` 与 `Iterator` 分别属于哪个 object？ | Container 提供 iterator；每个 iterator 保存一次遍历进度。 |
| 非 static inner iterator 的 `this` 指谁？ | 当前 iterator；用 `OuterClass.this` 表示关联的 outer object。 |
| Inner iterator 为什么能读 private array？ | Lexical access rule 赋予权限，enclosing instance 确定目标 object。 |
| 两个 iterator 是否复制两份 array？ | 本文设计没有；共享 container，各自保存 cursor。 |
| Static nested class 能读 private outer field 吗？ | 能，但 instance field 需要明确的 outer object reference。 |
| Private iterator class 为什么能返回给 client？ | 返回类型是公开 interface，client 通过 interface 调用。 |
| `private final T[] items` 代表内容不可变吗？ | 不代表；final 限制 reference 重赋值，不冻结 array slots。 |
| 为什么 linked iterator 不应反复 `get(i)`？ | 可能导致完整遍历 O(n²)，沿 links 推进是 O(n)。 |
| `equals(Deque61B<T>)` override 了 Object.equals 吗？ | 没有；需要 `equals(Object)`。 |
| `compare(a,b)==0` 是否意味着 `a.equals(b)`？ | 不一定；排序规则可能只比较部分属性。 |
| 找 maximum 为什么不初始化成 0？ | 输入可能全负，且 generic type 不一定是数字。 |
| GuitarString 的有效长度与 array capacity 谁影响音高？ | 有效 sample 数量决定主要循环延迟。 |
| `sample()` 与 `tic()` 的差别是什么？ | 一个读取状态，一个推进状态。 |

## 14. 参考资料

- [Project 1C Specification](https://sp24.datastructur.es/projects/proj1c/)：任务与实现约束。
- [Project 1C FAQ](https://sp24.datastructur.es/projects/proj1c/faq/)：package 等问题。
- [Java Iterable](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Iterable.html)：可遍历对象的 contract。
- [Java Iterator](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Iterator.html)：遍历、耗尽和 optional removal。
- [Java Language Specification（JLS）§8.1.3](https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html#jls-8.1.3)：inner class 与 enclosing instance。
- [JLS §6.6.1](https://docs.oracle.com/javase/specs/jls/se17/html/jls-6.html#jls-6.6.1)：访问权限的正式规则。
- [Oracle Nested Classes Tutorial](https://docs.oracle.com/javase/tutorial/java/javaOO/nested.html)：nested class、shadowing、qualified this 示例。该教程基于 Java 8，旧版本限制不应一概套用到新版本；具体语言规则以对应 JLS 为准。
- [Java Object](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Object.html)：equals、hashCode、toString。
- [Java Type Erasure](https://docs.oracle.com/javase/tutorial/java/generics/erasure.html)：generic type 的编译处理。
- [Java Pattern Matching for instanceof](https://docs.oracle.com/en/java/javase/17/language/pattern-matching-instanceof.html)：类型匹配与 pattern variable。
- [Java Inheritance](https://docs.oracle.com/javase/tutorial/java/IandI/subclasses.html)：subclass 与成员复用。
- [Java Comparable](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Comparable.html)、[Java Comparator](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Comparator.html)：自然顺序与外部比较规则。
- [Princeton Guitar String Assignment](https://introcs.cs.princeton.edu/java/assignments/guitar.html)：ring buffer 与 Karplus–Strong 背景。
- [Truth IterableSubject](https://truth.dev/api/latest/com/google/common/truth/IterableSubject.html)：集合内容与顺序 assertion。
