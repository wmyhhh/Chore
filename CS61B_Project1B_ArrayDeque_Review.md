# CS 61B Project 1B：`ArrayDeque61B` 知识梳理

> 主要依据：[Project 1B Specification](https://sp24.datastructur.es/projects/proj1b/)、[Project 1B FAQ](https://sp24.datastructur.es/projects/proj1b/faq/)、[Coverage Flags](https://sp24.datastructur.es/projects/proj1b/flags/) 与当前仓库中的 `skeleton-sp24/proj1b`。
>
> 本文聚焦 conceptual model、representation invariant、complexity、testing strategy 与常见错误，不给出一份可直接提交的完整 implementation。Project 1B 要求独立完成，最终代码应由自己根据这些原则设计并验证。

---

## 1. 这个 Project 究竟在训练什么

Project 1B 要实现一个以 Java array 为 **backing data structure（底层存储结构）** 的 `Deque61B<T>`。`Deque` 是 **Double-Ended Queue（双端队列，读作 “deck”）**，支持从 front 和 back 两端添加、删除元素。

表面任务是实现若干 methods，真正的学习主线是：

1. 把 ADT 的 logical order 映射到 array 的 physical indices；
2. 用 **circular array（循环数组）** 消除每次两端操作时的整体搬移；
3. 用 **geometric resizing（几何扩容/缩容）** 同时满足 time 与 space 要求；
4. 通过 **representation invariant（表示不变式）** 管理 mutable state；
5. 使用 **TDD（Test-Driven Development，测试驱动开发）** 和 edge-case tests 验证 stateful data structure；
6. 区分 worst-case time 与 **amortized time（摊还时间）**。

一句话概括：

> Project 1A 让你用 linked nodes 表达 deque；Project 1B 让你用 circular, resizable backing array 表达同一个 ADT，并理解不同 representation 如何改变 performance 与 implementation difficulty。

---

## 2. ADT、API、Interface 与 Implementation

### 2.1 四个概念不要混在一起

- **ADT（Abstract Data Type，抽象数据类型）**：描述数据的 logical behavior，例如 deque 可以在两端 add/remove。
- **API（Application Programming Interface，应用程序编程接口）**：method signature、Javadoc、return value、invalid input behavior 与 complexity requirement。
- **Interface**：Java 中表达 API contract 的一种 type，例如 `Deque61B<T>`。
- **Implementation**：满足 contract 的具体 class，例如 `LinkedListDeque61B<T>` 或 `ArrayDeque61B<T>`。

因此：

```java
Deque61B<String> deque = new ArrayDeque61B<>();
```

- variable 的 **static type（静态类型）** 是 `Deque61B<String>`；
- object 的 **dynamic type（运行时类型）** 是 `ArrayDeque61B<String>`；
- 调用者依赖 interface contract，不应依赖 backing array 的具体排布。

这体现了 **polymorphism（多态）** 和 **abstraction barrier（抽象屏障）**。

### 2.2 本地 `Deque61B<T>` 的 method contracts

| Method | Logical behavior | Invalid/empty case | Target complexity |
|---|---|---|---:|
| `addFirst(T x)` | 在 front 添加 | spec 假设 `x` 非 `null` | amortized $O(1)$ |
| `addLast(T x)` | 在 back 添加 | spec 假设 `x` 非 `null` | amortized $O(1)$ |
| `removeFirst()` | 删除并返回 front | empty 时返回 `null` | amortized $O(1)$ |
| `removeLast()` | 删除并返回 back | empty 时返回 `null` | amortized $O(1)$ |
| `get(int index)` | 按 logical index 读取 | negative 或 `index >= size` 时返回 `null` | $O(1)$ |
| `size()` | 返回 logical element count | empty 时为 `0` | $O(1)$ |
| `isEmpty()` | 判断 logical size 是否为 `0` | — | $O(1)$ |
| `toList()` | 返回按 logical order 排列的新 `List` | empty 时为空 `List` | $O(n)$ |
| `getRecursive(int index)` | 为 interface consistency 保留 | 按当前 spec 的指定方式处理 | 不作为本项目核心 |

`n` 表示当前 logical element count，而不是 backing array capacity。

### 2.3 版本差异：以本地 skeleton 为准

当前本地文件 `skeleton-sp24/proj1b/src/Deque61B.java` 明确声明了 `isEmpty()` 和 `getRecursive()`。网页 FAQ 中有两条回答与该 skeleton/主 spec 不完全一致，可能来自其他学期或版本：

- 不要因为 FAQ 的旧说法而擅自删除或修改 `Deque61B.java`；
- 是否使用 `@Override`，由当前 interface 中是否存在对应 signature 决定；
- 出现冲突时，优先级应是：当前本地 skeleton 与 grader contract → 当前主 spec → FAQ。

---

## 3. `ArrayDeque` 与 `LinkedListDeque` 的对比

| Dimension | Array-backed deque | Linked-list-backed deque |
|---|---|---|
| Physical representation | 连续 array slots | 分散的 node objects 和 links |
| Front/back operation | circular indexing 后为 amortized $O(1)$ | 已知 ends 时为 $O(1)$ |
| Indexed access | $O(1)$ | 通常 $O(n)$ traversal |
| Resize | 偶尔需要 $O(n)$ copy | 不需要整体 resize |
| Per-element overhead | 通常较低，但可能有 unused slots | 每个 node 还保存 links |
| Locality | 较好的 cache locality | 通常较差 |
| Main invariant | size、capacity、boundary indices、logical-to-physical mapping | sentinel、links、connectivity、size |

这里最重要的思想是：同一个 ADT 可以有多个 implementations；API behavior 相同，不代表内部 representation 或 performance 相同。

---

## 4. Java 前置知识

### 4.1 Generic class 与 `implements`

```java
public class ArrayDeque61B<T> implements Deque61B<T> {
    // ...
}
```

- `T` 是 **type parameter（类型参数）**，使一个 class 能保存多种 reference types；
- `String`、`Integer` 等实际替代 `T` 的类型叫 **type argument（类型实参）**；
- `implements Deque61B<T>` 表示 class 承诺提供 interface 中要求的 methods；
- `@Override` 让 compiler 检查 method signature 是否真正满足 inherited contract；
- `ArrayDeque61B<int>` 不合法，因为 generic type argument 不能是 primitive type；应使用 wrapper class `Integer`。

### 4.2 为什么不能直接 `new T[8]`

Java generics 主要依赖 **type erasure（类型擦除）**；runtime 通常不知道 `T` 的实际类型，而 Java array 会在 runtime 保留并检查 component type。因此不能直接 instantiate `new T[...]`。

Project 允许的典型 workaround 是先创建 `Object[]`，再进行 unchecked cast：

```java
T[] items = (T[]) new Object[8];
```

这里的 warning 不应被理解为“compiler 已经证明安全”，而是 programmer 承担维护 type safety 的责任：不要通过其他 raw/aliased reference 把错误类型放入该 array。相关语言背景可参考 [Oracle Generics Restrictions](https://docs.oracle.com/javase/tutorial/java/generics/restrictions.html)。

### 4.3 Array、References 与 Memory Management

#### 4.3.1 Array 本身也是 object

Java array 本身是一个 object；`ArrayDeque61B` object、backing array 和实际 elements 通常是彼此独立的 objects。准确的 physical layout 由 JVM（Java Virtual Machine，Java 虚拟机）决定，但可以使用下面的 reference graph 理解程序语义：

```text
ArrayDeque61B<Dog> object
┌──────────────────────────────┐
│ size = 2                     │
│ nextFirst = ...              │
│ nextLast  = ...              │
│ items ───────────────────────┼──┐
└──────────────────────────────┘  │
                                  ▼
                         backing array object
                  ┌──────┬──────┬──────┬──────┐
physical index    │  0   │  1   │  2   │  3   │
                  ├──────┼──────┼──────┼──────┤
slot content      │ ref  │ ref  │ null │ null │
                  └──┬───┴──┬───┴──────┴──────┘
                     │      │
                     ▼      ▼
                  Dog A   Dog B
```

- `items` field 保存 backing array 的 reference；
- `items[0]` 保存 `Dog A` 的 reference；
- `Dog A` object 不存放在 `ArrayDeque61B` field 或 array slot 内；
- `size` 是 primitive metadata，描述 logical element count。

#### 4.3.2 Primitive array 与 reference array

Primitive array 的 slot 直接保存 primitive value：

```java
int[] numbers = new int[4];
numbers[0] = 42;
```

```text
numbers → [42, 0, 0, 0]
```

Reference array 的 slot 保存 reference 或 `null`：

```java
Dog[] dogs = new Dog[4];
dogs[0] = new Dog("Mochi");
```

```text
dogs → [ref, null, null, null]
          │
          ▼
     Dog("Mochi")
```

因此 `ArrayDeque61B<Integer>` 保存的是 `Integer` references，不是直接保存 primitive `int`；primitive argument 可以通过 **autoboxing（自动装箱）** 转换成 wrapper object。

#### 4.3.3 Reference assignment、aliasing 与 object identity

Reference assignment 复制的是 reference value，不会复制 object：

```java
Dog first = new Dog("Mochi");
Dog second = first;
items[0] = first;
```

```text
first ─────┐
second ────┼──→ one Dog("Mochi") object
items[0] ──┘
```

这种多个 references 指向同一个 object 的关系叫 **aliasing（别名关系）**。如果 object 是 mutable，通过任意一个 reference 修改它，其他 references 观察到的都是同一个 object 的变化。

这也解释了为什么向 deque 添加 object 通常不意味着 deep copy；data structure 保存 caller 提供的 reference，并保留原 object identity。

#### 4.3.4 `size` 只描述 logical state

假设 remove 前的状态是：

```text
logical deque: [Dog A, Dog B]

backing array:
index        0       1       2       3
           ┌───────┬───────┬──────┬──────┐
items      │ ref A │ ref B │ null │ null │
           └───────┴───────┴──────┴──────┘

size = 2
```

如果 `removeFirst()` 只执行 `size--`，API 可能把 logical state 解释成只剩 `Dog B`，但 physical array 仍然保存 `ref A`：

```text
logical deque: [Dog B]
size = 1

physical array: [ref A, ref B, null, null]
```

`size` 是 programmer 定义的 metadata。Garbage Collector 不会根据 `size`、`nextFirst` 或 deque API 推断某个 slot 是否已经失效；它只追踪真实存在的 references。

#### 4.3.5 Reachability 与 GC Roots

Garbage Collector（GC，垃圾回收器）从一组 **GC Roots（垃圾回收根）** 出发，沿 references 遍历 object graph。GC Roots 通常包括 active method calls 中的 references、thread stacks 可访问的 variables、`static` fields、JNI（Java Native Interface）references 和某些 JVM internal references。

如果 remove 后旧 slot 没有被清理，仍存在路径：

```text
GC Root
   │
   ▼
ArrayDeque61B object
   │ items
   ▼
backing array
   │ stale slot
   ▼
removed Dog object
```

因此 removed object 仍然 **reachable（可达）**，GC 不能回收它。对 GC 而言，“合法 deque element”和“已经逻辑删除但仍被 stale reference 指向的 object”没有区别。

#### 4.3.6 Remove 必须同时维护 logical correctness 与 memory correctness

Remove 的 reference 处理在概念上承担三种职责：

```java
T removed = items[physicalIndex]; // 保存要返回的 reference
items[physicalIndex] = null;      // 删除 deque 持有的 reference
size--;                           // 更新 logical metadata
```

实际 statement order 必须与你选择的 boundary invariant 一致，但三件事都不能遗漏：

1. 找到并保存 removed element；
2. 清除 backing array 中的 stale reference；
3. 更新 `size` 和相应 boundary。

如果 caller 接收返回值：

```java
Dog removedDog = deque.removeFirst();
```

那么 deque 不再引用 `Dog`，但 caller 的 `removedDog` 仍然引用它：

```text
backing array slot ──X──→ Dog A
removedDog ─────────────→ Dog A
```

这是正确行为。只有当 caller、其他 objects 和所有 GC Roots 都不再能到达 `Dog A` 时，它才 **eligible for garbage collection（具备垃圾回收资格）**。Eligible 不等于立刻释放；实际 collection time 由 JVM 决定。

#### 4.3.7 清除 reference 不等于销毁 object

执行 `items[index] = null` 只删除一条 reference edge。如果仍有 aliases：

```text
owner ────────→ Dog A
favoriteDog ──→ Dog A
items[index] ──X──→ Dog A
```

`Dog A` 仍然 reachable。因此要区分三个事件：

| Event | 含义 |
|---|---|
| Clear a reference | 某个 variable/slot 不再指向 object |
| Object becomes unreachable | 不再存在从任何 GC Root 到该 object 的 path |
| GC reclaims memory | JVM 在之后某个时间实际回收 object 占用的 memory |

#### 4.3.8 Loitering 与 memory leak

**Loitering（对象滞留）** 指 object 在程序逻辑上已经无用，却仍被不必要的 reference 保持 reachable。例如 deque 已经 remove 了大量大 objects，但 unused array slots 仍保存这些 references。

Java 会自动管理 memory，但 GC 只能回收 unreachable objects，不能判断一个 reachable reference 是否在业务逻辑上已经无用。这种长期的 unintended retention 属于广义的 **memory leak（内存泄漏）**，可能造成：

- heap usage 增长；
- GC 运行更频繁；
- application pause 增加；
- 严重时产生 `OutOfMemoryError`。

所以 Project 1B 的 memory requirement 不仅要求适时 shrink backing array，也要求 remove 后清除 element reference。Shrink 解决 unused capacity 过大；清 slot 解决 dead logical element 仍被 deque 引用。两者不能互相替代。

#### 4.3.9 Resize 复制的是 references

Resize 时通常复制 logical elements 的 references，而不是 deep-copy elements：

```text
oldItems[0] ──→ Dog A ←── newItems[0]
```

这是 **shallow copy（浅拷贝）**：新旧 slots 暂时指向同一个 `Dog A` object。完成 `items = newItems` 后，如果没有其他 reference 指向旧 backing array，旧 array 会变成 unreachable；它及其 slots 最终可以被 GC 回收。

Resize 不应 deep-copy elements，否则会改变 object identity，也可能改变 aliasing semantics。Copy 的对象是 logical element references，必须只复制当前 `size` 个有效 elements，不能把 unused slots 中可能存在的 stale references 当作 logical contents。

#### 4.3.10 Array 的 $O(1)$ access 与 locality

Array slots 在概念上具有固定宽度，JVM 可以根据 index 直接定位：

```text
slot location ≈ array base + index × slot width
```

因此 `items[index]` 不需要像 linked list 一样逐个 traversal，访问 array slot 是 $O(1)$。对于 reference array，连续排列的是 reference slots；references 指向的 objects 本身不保证在 heap 中连续：

```text
backing array slots
┌──────┬──────┬──────┐
│ ref1 │ ref2 │ ref3 │
└──┬───┴──┬───┴──┬───┘
   │      │      │
   ▼      ▼      ▼
 object  object  object
```

Array-backed structure 通常具有较好的 **locality（局部性）**，但读取 element object 仍需要 dereference slot 中的 reference。

本节最重要的结论是：

> `size` 决定 element 是否属于 deque 的 logical contents；array slot 是否仍保存 reference，决定该 object 是否可能继续被 GC 视为 reachable。

因此 remove 必须同时保证：

- **Logical correctness**：return value、logical order、`size` 和 boundaries 正确；
- **Memory correctness**：deque 不再保留 removed element 的 stale reference。

### 4.4 `Math.floorMod` 与 `%`

Circular indexing 需要把任何整数 index 规范化到 `[0, capacity)`。Java 的 `%` 是 remainder operator，负 dividend 可能产生负结果；`Math.floorMod(a, b)` 在 `b > 0` 时更适合得到非负 circular index。

```text
Math.floorMod(-1, 8) = 7
Math.floorMod(8, 8)  = 0
Math.floorMod(10, 8) = 2
```

Oracle 将它定义为 `x - floorDiv(x, y) * y`；详见 [`Math.floorMod`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Math.html#floorMod(int,int))。

`java.lang` 会自动 imported，因此通常不必显式写 `import java.lang.Math;`。

---

## 5. Circular Array 的 conceptual model

### 5.1 Logical order 不等于 physical order

假设 capacity 为 `8`，deque 的 logical contents 是：

```text
[A, B, C, D]
```

它在 backing array 中可能是：

```text
physical index:  0   1   2   3   4   5   6   7
array slot:      C   D   ·   ·   ·   ·   A   B

logical order:   A → B → C → D
physical walk:   6 → 7 → 0 → 1
```

因此 `get(0)` 不能简单返回 `items[0]`。它必须先把 logical index 转成 physical index。

### 5.2 为什么必须 circular

如果 front 永远绑定在 physical index `0`，那么 `addFirst` 可能需要把所有元素右移，单次操作为 $O(n)$。Circular design 允许 front 在 array 中移动：

- 到达最右侧后，下一步回到 index `0`；
- 到达 index `0` 后，向左一步回到最后一个 slot；
- 普通 add/remove 只修改一个 slot、少量 indices 和 `size`。

这让不触发 resize 的两端操作保持 $O(1)$。

### 5.3 一种推荐 boundary model

Spec/FAQ 推荐维护 `nextFirst` 和 `nextLast`。一种常见语义是：

- `nextFirst`：front element 之前的 empty slot；
- `nextLast`：back element 之后的 empty slot。

注意：它们指向的是“下一次可写入的位置”，不一定指向现有 element。

采用该语义时，应能从 invariant 推导出：

```text
front physical index       = next position after nextFirst
back physical index        = next position before nextLast
logical index i 的位置      = front position 向后移动 i 步
```

如果 capacity 为 `c`，一种数学表达是：

$$
physical(i) = \operatorname{floorMod}(nextFirst + 1 + i, c)
$$

这只是一个 representation choice，不是唯一设计。你也可以让 fields 直接指向 front/back elements，但必须为所有 methods 使用同一套语义，不能在不同 method 中混用。

---

## 6. Representation Invariant：真正的核心

**Representation invariant** 是 constructor 和每个 public method 返回时都必须成立的内部规则。对于采用 backing array、`size`、`nextFirst`、`nextLast` 的设计，至少应检查：

1. `items != null`；
2. `items.length >= 8`；
3. `0 <= size <= items.length`；
4. boundary indices 始终落在合法 physical range；
5. 从 front 起按 circular order 恰好能读取 `size` 个 logical elements；
6. `get(i)`、`toList()` 与两端操作使用相同的 logical-to-physical mapping；
7. removed slots 不继续保存已删除 element 的 reference；
8. full state 与 empty state 不能只靠 indices 猜测，`size` 必须消除 ambiguity；
9. resize 前后 logical contents 与 order 不变；
10. capacity 较大时满足 spec 的 usage-factor requirement。

### 为什么 `size` 很重要

在 circular array 中，两个 boundary indices 的某种相对关系可能既表示 empty，也可能表示 full。显式维护 `size` 可以：

- $O(1)$ 返回 `size()`；
- $O(1)$ 实现 `isEmpty()`；
- 区分 empty 与 full；
- 快速判断 invalid `get`；
- 判断何时 grow 或 shrink。

---

## 7. 各 method 应该怎样思考

以下内容给出 design reasoning，不给出完整 source code。

### 7.1 Constructor

Constructor 返回前必须建立初始 invariant：

- backing array capacity 为 spec 要求的 `8`；
- logical `size` 为 `0`；
- 两个 boundary indices 处于一个彼此一致的 empty configuration；
- 不应创建额外的 built-in data structure 作为 field。

不要只问“indices 初始值是什么”，应问：选择这些值后，第一次 `addFirst`、第一次 `addLast`、empty `get` 和 empty remove 是否都能自然工作？

### 7.2 `addFirst` / `addLast`

每次普通 add 的 conceptual steps 是：

1. 若 array 已满，先 grow；
2. 在对应 boundary 的 available slot 写入 element；
3. 将 boundary 向外移动一格并 wrap around；
4. `size` 增加 `1`。

关键不是死记 step order，而是确保写入的位置和更新后的 boundary semantics 一致。两种合法设计可能采用不同 update order；混合两种设计通常产生 off-by-one error。

**约束：**除 resize 外，single add 不得 loop 或 recurse，应为 $O(1)$。

### 7.3 `get`

先进行 logical bounds check：

```text
index < 0           → invalid
index >= size       → invalid
otherwise           → map logical index to physical index
```

比较对象是 `size`，不是 `items.length`。Unused capacity 不是 deque 的 logical contents。

有效 `get` 只做 arithmetic 和一次 array access，所以必须为 $O(1)$；不应从 front 循环走 `index` 步。

### 7.4 `size` / `isEmpty`

- `size()` 直接读取维护好的 metadata；
- `isEmpty()` 应由 logical size 推导，而不是扫描 array 中是否全为 `null`。

扫描 array 不仅是 $O(n)$，还会把“unused slot 为 `null`”错误地当成 API semantics。即使当前 spec 假设 add 的元素非 `null`，representation 也不应通过扫描确定 logical size。

### 7.5 `toList`

`toList()` 应创建并返回一个新的 `List<T>`，按 logical front-to-back order 放入恰好 `size` 个 elements。这里是 implementation 中被明确允许使用 `ArrayList` 的位置。

理想思路：

```text
for each logical index i from 0 to size - 1:
    read the corresponding logical element
    append it to a new result list
```

它应为 $O(n)$，不得改变 deque state。Spec 禁止在 `ArrayDeque61B` 内部的其他 methods 调用 `toList()`，否则容易隐藏额外的 $O(n)$ work 并违反 timing constraints。

### 7.6 `removeFirst` / `removeLast`

每次普通 remove 要回答四个问题：

1. empty 时是否立即返回 `null`，且 state 不变？
2. 哪个 physical slot 是要删除的 logical end？
3. 何时移动 boundary，何时更新 `size`？
4. 是否把 removed slot 清为 `null`，消除 stale reference？

若按 `nextFirst` / `nextLast` 表示空闲边界，则 remove 与 add 在结构上是 mirror operations：add 从边界向外扩张，remove 向 logical contents 内收缩。

**约束：**除 shrink 外，single remove 不得 loop 或 recurse，应为 $O(1)$。

### 7.7 `getRecursive`

这个 method 在 array-backed implementation 中没有教学价值；Project 1B 主 spec 给出了指定的 unsupported behavior。按本地 interface 和当前 spec 处理，不要为“递归而递归”写一个 $O(n)$ implementation。

---

## 8. Resizing：最容易出错的部分

### 8.1 Grow 的触发与目标

当 `size == items.length` 时 backing array 已满，下一次 add 前必须 grow。Spec 要求按 geometric factor 增长，例如容量成倍增加，而不是每次只增加常数。

Resize 必须保持：

```text
before logical order == after logical order
before size          == after size
```

一个容易验证的 strategy 是把旧 deque 按 logical index `0 ... size - 1` 复制到新 array 的一段连续区域，然后重新建立 boundary indices。不要直接假设旧 array 中的 elements 本来就是连续或从 index `0` 开始。

### 8.2 为什么 geometric growth 很重要

若 capacity 每次只加常数，构造 $n$ 个 elements 可能发生约 $n$ 次 copy，总代价近似：

$$
1 + 2 + 3 + \cdots + n = \Theta(n^2)
$$

若每次按倍数 grow，copy 规模形成 geometric series：

$$
1 + 2 + 4 + \cdots + n < 2n = \Theta(n)
$$

因此，虽然某一次触发 resize 的 add 是 $O(n)$，连续 $n$ 次 adds 的总 resize work 仍是 $O(n)$，single add 的 **amortized complexity（摊还复杂度）** 为 $O(1)$。

### 8.3 Shrink 与 usage factor

定义：

$$
usageFactor = \frac{size}{capacity}
$$

Spring 2024 spec 要求：

- 当 array length 至少为 `16` 时，usage factor 不应长期低于 `25%`；
- 按该版 spec 的精确措辞，在执行 remove 前，若当前 `size <= 25% * capacity` 且 capacity 至少为 `16`，应先 shrink，再完成 remove；
- 小 array 可以保持低 usage，实际设计通常保留 minimum capacity `8`；
- shrink 也必须用 geometric factor，而不是一次减少一个 slot。

阈值判断尽量使用 integer arithmetic，避免不必要的 floating-point comparison。例如思考 `size * 4 <= capacity` 所表达的条件，同时确认 multiplication overflow 在当前 project scale 下是否构成实际风险。

### 8.4 为什么 grow 与 shrink 不能使用同一个 threshold

若 grow 和 shrink 都在相同 utilization 附近触发，少量 add/remove 可能造成 capacity 反复变化，称为 **thrashing（抖动）**。本项目的典型 policy 是：

- full 时 grow；
- 低到 `25%` 左右才 shrink。

中间保留一段 **hysteresis（滞回区间）**，避免频繁 copy。

### 8.5 一个 resize helper 应承担什么责任

一个好的 private helper 通常只做 representation-level work：

1. allocate new array；
2. 按 logical order shallow-copy 当前 `size` 个 element references，不复制 objects 本身；
3. 替换 backing array reference；
4. 重新设置 boundary indices；
5. 保持 logical `size` 不变。

调用 helper 的 add/remove method 再完成自己的业务操作。这样 grow 与 shrink 共享同一套 copy 逻辑，减少 duplicate bugs。

---

## 9. Complexity 总表

令 `n = size`：

| Operation | Worst case | Amortized | Why |
|---|---:|---:|---|
| `addFirst` | $O(n)$ | $O(1)$ | 普通情况常数操作，偶尔 grow copy |
| `addLast` | $O(n)$ | $O(1)$ | 同上 |
| `removeFirst` | $O(n)$ | $O(1)$ | 普通情况常数操作，偶尔 shrink copy |
| `removeLast` | $O(n)$ | $O(1)$ | 同上 |
| `get` | $O(1)$ | $O(1)$ | arithmetic + one array access |
| `size` | $O(1)$ | $O(1)$ | 读取 metadata |
| `isEmpty` | $O(1)$ | $O(1)$ | 检查 metadata |
| `toList` | $O(n)$ | $O(n)$ | 必须复制所有 logical elements |
| resize helper | $O(n)$ | — | copy 当前 elements |

Space complexity 在 capacity 与 `n` 保持常数比例时为 $O(n)$。Minimum capacity 导致 empty/small deque 仍使用固定常数空间，但 asymptotically 仍满足要求。

---

## 10. Testing Strategy：从 contract 推导 tests

### 10.1 TDD 的基本循环

**TDD（Test-Driven Development）** 的经典循环是：

1. **Red**：先写一个针对明确 behavior 的 test，并确认它失败；
2. **Green**：写最少 implementation 使 test 通过；
3. **Refactor**：在 tests 保护下整理 duplication、naming 与 helper boundaries。

本地 tests 使用 JUnit 5 的 `@Test` 发现 test method，并使用 Google Truth 编写 assertions。基础形式是：

```java
assertThat(actual).isEqualTo(expected);
```

对 list contents 和 order，可使用：

```java
assertThat(actualList)
        .containsExactlyElementsIn(expectedList)
        .inOrder();
```

测试细节可配合阅读同目录的 [Project 1A Testing 复习笔记](./CS61B_Project1A_Testing_Review.md)。

### 10.2 每个 test 应验证三类东西

对 mutable data structure，一次 operation 后最好同时检查：

- **Return value**：返回的 element 或 `null` 是否正确；
- **Observable state**：`size`、`isEmpty`、`get`、`toList` 是否正确；
- **Future behavior**：接下来继续 add/remove 是否仍正确。

第三类尤其重要：某个 method 可能返回正确结果，却悄悄破坏 boundary index，直到下一次 operation 才暴露。

### 10.3 Coverage flags 转化为 scenario matrix

官方 coverage flags 可以整理成以下最小 scenario families：

| Family | 必测 scenarios |
|---|---|
| Add | `addFirst` / `addLast` from empty、from nonempty、trigger grow |
| Add after remove | remove to empty 后再次从两端 add |
| Remove | 两端 remove、remove to one、remove last item、empty remove |
| Shrink | `removeFirst` / `removeLast` 触发 shrink；grow 后再 shrink |
| Get | first/middle/last valid index、negative index、`index == size`、large index、empty |
| Size | constructor 后、mixed adds 后、remove 后、remove to empty 后、empty remove 后 |
| isEmpty | empty 为 true；add 后 false；remove to empty 后恢复 true |
| toList | empty、nonempty、mixed front/back operations、wraparound、resize 前后 |

Coverage flag 只说明“执行过哪些 scenarios”，不保证 assertions 正确，也不保证所有 correctness cases 已覆盖。

### 10.4 高价值 operation sequences

不要只测试单个 method；应测试会穿过多种 internal states 的 sequences：

```text
empty
→ add until full
→ trigger grow
→ remove from both ends
→ wrap around
→ remove to low utilization
→ trigger shrink
→ remove to empty
→ add again
```

另一个重要模式是 mixed operations：

```text
addFirst → addLast → addFirst → removeLast → addLast → removeFirst
```

每一步维护一个手写的 expected logical list，并与 `toList()` 对比。

### 10.5 Boundary values

重点测试 threshold 附近，而不是只测远离边界的普通值：

- size `0`、`1`；
- size `capacity - 1`、`capacity`；
- `get(-1)`、`get(0)`、`get(size - 1)`、`get(size)`；
- usage factor 刚高于、等于、刚低于 `25%`；
- physical index 从 `0` wrap 到 `capacity - 1`，以及反方向 wrap。

---

## 11. Debugging：围绕 invariant，而不是猜代码

### 11.1 建议画四张图

对每个 bug，画出以下 states 的 backing array：

1. empty；
2. one element；
3. wrapped non-full；
4. full immediately before resize。

图上同时标出：

```text
physical indices
items in each slot
nextFirst
nextLast
size
logical front/back
```

如果无法在纸上准确指出 `get(0)` 和 `get(size - 1)` 位于哪里，说明 representation semantics 还没有定义清楚。

### 11.2 每次 operation 后做 invariant checklist

调试时可暂时添加 private validation/helper 或 debugger watches，检查：

- `size` 是否只改变一次；
- boundary 是否 move 到预期 slot；
- wrap 后 index 是否仍合法；
- logical order 是否不变；
- remove 后旧 slot 是否为 `null`；
- resize 后所有 elements 是否恰好 copy 一次；
- resize 后第一和最后 logical element 是否可由 `get` 正确读取。

### 11.3 定位“第一次坏掉”的时刻

不要只查看 long sequence 的最终 failure。让 test 在每一步都 assert `toList()`、`size()` 和关键 `get()`，使用 binary reduction 或逐步缩短 operation sequence，找到 invariant 第一次被破坏的位置。

### 11.4 常见 exception 的含义

- `ArrayIndexOutOfBoundsException`：wraparound 或 off-by-one 通常有误；
- `NullPointerException` / unboxing error：expected element slot 中实际为 `null`，通常源于 index update 或 resize copy 漏项；
- `ExecutionTimeoutException`：可能使用 additive resizing、无限 loop，或在应为 $O(1)$ 的 method 中 traversal/copy；
- coverage 不增长：较早 test 的 incorrect assertion 可能提前终止整个 test method，后续 scenarios 没有执行。

---

## 12. 高频错误与原因

### 12.1 `get(0)` 直接返回 `items[0]`

错误原因：把 logical index 当作 physical index；front 不保证位于 slot `0`。

### 12.2 每次 `addFirst` 都移动所有元素

错误原因：没有采用 circular representation，导致 $O(n)$ ordinary add，timing test 会失败。

### 12.3 使用 `(index - 1) % capacity`

错误原因：Java remainder 对负数可能返回负值；应使用 `floorMod` 或确保先加 capacity 再取模。

### 12.4 用 `items.length` 判断 `get` 是否越界

错误原因：capacity 不是 logical size，unused slots 不是 deque elements。

### 12.5 Resize 按 physical index 原样 copy

错误原因：wrapped array 的 physical order 可能不是 logical order；resize 后 deque 顺序被旋转或打乱。

### 12.6 Resize 后忘记重建 boundaries

错误原因：new array 的布局变了，旧 indices 不再描述新的 representation。

### 12.7 Remove 只减 `size`，不清 slot

错误原因：产生 stale reference/loitering，不满足 memory correctness。

### 12.8 Empty remove 仍然移动 indices

错误原因：empty operation 应返回 `null` 且不改变 state；否则“remove from empty → add”会暴露问题。

### 12.9 Grow 使用 `capacity + constant`

错误原因：大量 adds 的总 copy cost 退化为 $\Theta(n^2)$，可能 timeout。

### 12.10 在 `get`、`size` 或 `isEmpty` 中调用 `toList`

错误原因：把要求的 $O(1)$ operation 变成 $O(n)$；spec 也明确禁止内部调用 `toList()`。

### 12.11 只测试 return value，不测试后续 state

错误原因：boundary 或 size 已被破坏，但当前 return value 恰好正确；bug 延迟到下一次 operation 才出现。

---

## 13. 推荐完成顺序

官方建议先完成 fixed-capacity version，再处理 resizing。一个稳健顺序是：

1. 阅读本地 `Deque61B.java`，逐条写下 contract；
2. 明确 fields 的语义，并画出 empty / one-element / full states；
3. constructor；
4. `addFirst`、`addLast`，暂时只测不超过 capacity 的情形；
5. `get`；
6. `size`、`isEmpty`；
7. `toList`；
8. fixed-capacity `removeFirst`、`removeLast`；
9. 抽取 resize helper；
10. grow，并测试两种 add 都能触发；
11. shrink，并测试两种 remove、threshold 和 minimum capacity；
12. mixed-operation / wraparound / grow-then-shrink tests；
13. 处理 `getRecursive` 的 spec requirement；
14. 运行完整 tests、style checker，再使用有限的 autograder tokens。

每个阶段都遵循：先写 test 并确认失败，再实现，再跑全部 regression tests。

---

## 14. 提交前 Self-check Checklist

### API 与 style

- [ ] Class signature 正确使用 `<T>` 并 `implements Deque61B<T>`。
- [ ] 没有修改 `Deque61B.java`。
- [ ] 所有 required methods 的 signature 完全匹配。
- [ ] 没有把 built-in collections 用作 fields。
- [ ] `toList()` 是允许使用 `ArrayList` 的特殊位置。
- [ ] private helper 命名和职责清晰，style checker 通过。

### Correctness

- [ ] Constructor 建立 capacity `8` 的合法 empty state。
- [ ] 两端 add/remove 在 empty、one、many、wrapped states 都正确。
- [ ] `get` 对 valid、negative、too-large index 都正确。
- [ ] `toList` 返回新的 list，order 正确且不改变 deque。
- [ ] Empty remove 返回 `null` 且 state 不变。
- [ ] Remove 后对应 slot 不再保存 removed reference。
- [ ] Resize 前后 logical order、size 和 future behavior 一致。

### Performance 与 memory

- [ ] Ordinary add/remove 没有 loop 或 recursion。
- [ ] `get`、`size`、`isEmpty` 为 $O(1)$。
- [ ] `toList` 和 resize 为 $O(n)$。
- [ ] Grow/shrink 使用 geometric factor。
- [ ] Capacity 至少为 `16` 时满足 `25%` usage policy。
- [ ] Capacity 不会 shrink 到初始 minimum 以下。

### Tests

- [ ] 覆盖官方每一类 coverage flag，而不只是 method line coverage。
- [ ] 测试 wraparound、grow、shrink、grow then shrink。
- [ ] 测试 remove to empty 后重新 add。
- [ ] 测试 threshold 两侧的 boundary values。
- [ ] 每个 assertion 的 actual/expected 顺序正确。
- [ ] 本地 tests 与 style 都通过后才提交 autograder。

---

## 15. 核心术语速查

| English term | 含义 |
|---|---|
| Deque / Double-Ended Queue | 可从两端 add/remove 的双端队列 |
| ADT / Abstract Data Type | 只描述 logical behavior 的抽象数据类型 |
| API / Application Programming Interface | 调用者可见的 contract |
| Backing array | 保存实际 element references 的底层数组 |
| Circular array / Ring buffer | 末端与开头逻辑相邻的数组表示 |
| Logical index | 用户从 front 看到的 index |
| Physical index | element 在 backing array 中的实际 slot |
| Capacity | backing array 的 slot 数量 |
| Size | 当前 logical element 数量 |
| Representation invariant | 每次 public operation 前后必须成立的内部规则 |
| Geometric resizing | capacity 按乘法因子变化 |
| Amortized analysis | 把偶发昂贵操作分摊到一系列 operations 上分析 |
| Usage factor | `size / capacity` |
| Loitering | 已逻辑删除的 object 仍被 stale reference 持有 |
| Off-by-one error | index 边界相差一格的错误 |
| Wraparound | index 越过 array 端点后绕回另一端 |
| TDD / Test-Driven Development | 先写失败 test，再实现，再 refactor |
| Regression test | 防止已修复 behavior 再次损坏的测试 |
| Thrashing | capacity 因阈值设计不当而频繁 grow/shrink |

---

## 16. 最终知识地图

```text
Deque ADT
│
├── Java abstraction
│   ├── interface / implements / @Override
│   └── generics / type erasure / generic array workaround
│
├── Array representation
│   ├── backing array
│   ├── size and boundary indices
│   ├── circular indexing / floorMod
│   └── logical-to-physical mapping
│
├── Dynamic capacity
│   ├── geometric grow
│   ├── usage factor and shrink
│   ├── order-preserving copy
│   └── amortized O(1)
│
├── Memory correctness
│   ├── clear removed references
│   └── capacity proportional to current size
│
└── Verification
    ├── TDD and Truth assertions
    ├── boundary-value tests
    ├── state-transition sequences
    └── invariant-centered debugging
```

掌握这张图中的关系，Project 1B 就不再是八九个互相独立的 methods，而是“一套 representation invariant + 一套 logical-to-physical mapping + 一组维护它们的 operations”。

---

## 参考资料

- [CS 61B Spring 2024 — Project 1B Specification](https://sp24.datastructur.es/projects/proj1b/)
- [CS 61B Spring 2024 — Project 1B FAQ](https://sp24.datastructur.es/projects/proj1b/faq/)
- [CS 61B Spring 2024 — Project 1B Coverage Flags](https://sp24.datastructur.es/projects/proj1b/flags/)
- [CS 61B Spring 2024 — Project 1A Specification](https://sp24.datastructur.es/projects/proj1a/)
- [Oracle Java Tutorials — Generic Types](https://docs.oracle.com/javase/tutorial/java/generics/types.html)
- [Oracle Java Tutorials — Restrictions on Generics](https://docs.oracle.com/javase/tutorial/java/generics/restrictions.html)
- [Oracle Java SE API — `Math.floorMod`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Math.html#floorMod(int,int))
- [JUnit 5 — `@Test`](https://docs.junit.org/5.9.1/api/org.junit.jupiter.api/org/junit/jupiter/api/Test.html)
- [Google Truth API](https://truth.dev/api/latest/com/google/common/truth/Truth.html)
