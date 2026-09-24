# CS 61B Project 1A 前置知识复习速查

> 依据：[Project 1A Specification](https://sp24.datastructur.es/projects/proj1a/)、[CS 61B Spring 2024](https://sp24.datastructur.es/) 与我们后续关于 nested class、encapsulation、package、`extends` / `implements` 的讨论。
>
> 本文只总结 Java 与 data structure 前置知识，不包含 fields 设计、pointer 更新顺序、method algorithm 或其他 Project 1A 实现方案。

---

## 1. Project 1A 的知识主线

Project 1A 训练的是：根据一个 **Abstract Data Type（ADT，抽象数据类型）** 的 API contract，使用 linked representation 建立一个始终合法的 mutable object，并通过 testing 和 debugging 验证 correctness、time complexity 与 space usage。

| 知识模块 | 应掌握的核心问题 |
|---|---|
| ADT、API、implementation | 对外 behavior 与内部 representation 有什么区别？ |
| Java object model | variable 保存 object 还是 reference？aliasing 如何产生？ |
| class、interface、generics | 如何 declare 可存放多种 reference types 的 implementation？ |
| linked structure | node、link、sentinel、circular topology 和 invariant 是什么？ |
| complexity | 哪些 operations 是 $O(1)$，哪些通常需要 $O(n)$ traversal？ |
| testing、debugging | 如何从 contract 推导 tests，并定位 invariant 第一次被破坏的位置？ |

---

## 2. ADT、API、Implementation 与 Invariant

- **ADT** 描述数据在逻辑上是什么、支持哪些 operations，以及这些 operations 的 observable behavior。
- **API（Application Programming Interface）** 包括 method name、parameter、return type、Javadoc、特殊输入行为与性能要求。
- **Implementation** 是实现 API contract 的代码。
- **Representation** 是 object 内部保存 state 的方式；调用者不应依赖它。
- **Abstraction Barrier（抽象屏障）** 将“做什么”与“怎么做”分开。
- **Representation Invariant（表示不变式）** 是 constructor 和每个 public mutating method 返回时，内部 object graph 必须满足的条件。

**Deque（Double-Ended Queue，双端队列）** 支持在两端操作元素。它可以表达 FIFO（First In, First Out，先进先出）的 queue behavior，也可以表达 LIFO（Last In, First Out，后进先出）的 stack behavior。

阅读每个 interface method 时，应回答：有效输入是什么、返回什么、是否修改 state、empty/invalid case 如何处理、time complexity 有何要求。

---

## 3. Java Object Model

### 3.1 Primitive Type 与 Reference Type

- Primitive types：`int`、`boolean`、`char`、`double` 等，variable 保存 value 本身。
- Reference types：class、interface、array、`String` 等，variable 保存指向 object 的 reference。
- `null` 表示 reference 不指向 object；dereference `null` 会产生 `NullPointerException`。

```java
Widget first = new Widget();
Widget second = first;
```

这里只有一个 `Widget` object 和两个 references。`second = first` 不会 copy object，这种多个 references 指向同一 mutable object 的关系叫 **Aliasing（别名关系）**。

Java 永远使用 **Pass-by-Value（按值传递）**：primitive argument 复制 primitive value，object argument 复制 reference value。callee 可以通过复制的 reference 修改同一 object，但 reassignment parameter 不会改变 caller variable。

### 3.2 Class、Object、Field 与 Constructor

- `class` 定义 state 和 behavior；`object` 是运行时 instance。
- **Instance field** 每个 instance 各有一份；`static field` 属于 class，所有 instances 共享。
- **Local variable** 属于一次 method invocation，使用前必须 definite assignment。
- **Constructor** 与 class 同名且没有 return type；返回前应建立完整 invariant。
- `this` 表示当前 instance；`Outer.this` 表示 inner object 所绑定的 enclosing instance。

### 3.3 Garbage Collection

Garbage Collector（GC）只能回收 unreachable objects。一个 element 即使在逻辑上已经 removed，只要仍存在 reference path，它就依然 reachable。应避免 **Loitering（对象滞留）**，使 memory usage 与当前元素数量保持同阶，而不是与历史操作总量相关。

---

## 4. Generics

```java
public class Box<T> {
    private T item;
}

Box<String> words = new Box<>();
Box<Integer> numbers = new Box<>();
```

- `T` 是 **Type Parameter（类型参数）**，不是 runtime variable。
- `<>` 是 **Diamond Operator（菱形操作符）**，让 compiler 推断 type argument。
- Generic type 不能直接使用 primitive，如 `Box<int>`；应使用 wrapper class，如 `Box<Integer>`。
- 避免 `Box box` 这样的 **Raw Type（原始类型）**，否则会绕过部分 compile-time type checking。
- Non-static inner class 可以使用 outer class 的 type parameter；static nested class 不能隐式使用 outer `T`，如有需要必须 declare 自己的 type parameter。

---

## 5. Interface、`implements` 与 `extends`

### 5.1 Interface 与 Polymorphism

```java
SomeInterface<String> value = new SomeImplementation<>();
```

- variable 的 **Static Type（静态类型）** 是 `SomeInterface<String>`。
- object 的 **Dynamic Type（运行时类型）** 是 `SomeImplementation<String>`。
- 调用者依赖 interface contract，不必知道 representation，这体现 **Polymorphism（多态）**。
- `@Override` 让 compiler 检查 method signature 是否真正覆盖 interface/superclass method。

### 5.2 `extends` 与 `implements`

| 关系 | Syntax | 含义 |
|---|---|---|
| class → class | `class B extends A` | 继承 superclass type 和可继承 implementation；只能直接 extend 一个 class |
| class → interface | `class C implements I` | 承诺满足 interface contract；可 implements 多个 interfaces |
| interface → interface | `interface J extends I` | 继承、组合或细化 contracts；可 extend 多个 interfaces |

`extends class` 主要提供 **Implementation Inheritance（实现继承）**；`implements interface` 主要建立 capability/API contract 和 subtype relationship。Constructor 不会被继承，subclass constructor 使用 `super(...)` 初始化 superclass 部分。

Private method 对 subclass 不可见，也不会被真正 override；subclass 中同 signature 的 method 只是一个新的 method。只有确实满足 **is-a relationship** 时才使用 class inheritance；**has-a relationship** 通常更适合 **Composition（组合）**。

---

## 6. Nested Class：Static 与 Non-static

```text
Nested Class
├── Static Nested Class
└── Non-static Nested Class（Inner Class）
```

| 特性 | Non-static inner class | Static nested class |
|---|---|---|
| 是否绑定特定 outer object | 是，隐式保存 `Outer.this` | 否 |
| 能否直接访问 outer instance members | 能 | 不能 |
| 外部 instantiate syntax | `outer.new Inner()` | `new Outer.Nested()` |
| 是否可能延长 outer object lifetime | 可能 | 不会因 enclosing reference 而发生 |
| 典型用途 | helper object 需要特定 outer instance state | helper type 只在逻辑上属于 outer class |

Static nested class 仍可通过一个明确的 outer object reference 访问 outer private members；它缺少的只是隐式 `Outer.this`。如果 helper class 不需要 enclosing instance，通常优先 static nested class，以避免不必要的 coupling 和 hidden reference。

---

## 7. Encapsulation、Package 与 Access Control

**Encapsulation（封装）** 不只是把 fields 写成 `private`，而是把 state 与维护 state 的 operations 放在同一 abstraction boundary 内，防止外部代码绕过 operations 破坏 invariant。

### 7.1 Access Modifiers

| Access | 当前 class | 同 package | 不同 package 的 subclass | 任意调用者 |
|---|---:|---:|---:|---:|
| `private` | 是 | 否 | 否 | 否 |
| package-private（不写 modifier） | 是 | 是 | 否 | 否 |
| `protected` | 是 | 是 | 有条件 | 否 |
| `public` | 是 | 是 | 是 | 是 |

### 7.2 Package

```java
package com.example.bank;
```

Package 是组织相关 types 的 namespace 和 access boundary，通常对应 directory `com/example/bank/`。同一 package 的 classes 可以访问彼此的 package-private members。

- `com.example.bank` 与 `com.example.bank.internal` 是不同 packages。
- `import` 只允许简写 type name，不会改变当前 class 的 package，也不会授予 package-private access。
- Top-level class 只能是 `public` 或 package-private；nested class 才能 declare 为 `private` 或 `protected`。

### 7.3 什么时候使用 Private Method

如果 method 只是 validation、结构维护、重复逻辑抽取等 implementation detail，且调用者不需要独立使用它，通常应设为 `private`。采用 **Principle of Least Privilege（最小权限原则）**：默认选择满足需求的最严格 access level，只有确有协作需要时才放宽。

Private access 是 class-level，而非 instance-level：同一个 class 的代码可以访问另一个同类型 object 的 private members。Nested class 与 enclosing class 也可以互相访问 private members。

### 7.4 Representation Exposure

即使 field 是 `private`，直接返回内部 mutable object 的 reference 仍可能产生 **Representation Exposure（内部表示泄漏）**。必要时使用 **Defensive Copy（防御性复制）**、immutable value 或受限 view。`final` 只阻止 reference reassignment，不保证 referenced object immutable。

---

## 8. Linked Data Structure

- **Node** 通常组合 payload 与 links，linked structure 本质上是 object graph。
- **Singly Linked List（单向链表）** 主要提供一个 traversal direction。
- **Doubly Linked List（双向链表）** 提供两个 directions，但需要同时维护两侧 link consistency。
- **Sentinel Node（哨兵节点）** 是服务于 structure boundary 的特殊 node，不应与普通 logical element 混淆。
- **Circular Topology（环形拓扑）** 使用回到明确 boundary object 作为 traversal termination，而不是等待 `null`。

理解 linked structure 时应在纸上画 objects 和 arrows，分别检查 empty、single-element、multi-element states。每个 public operation 返回后，都要检查 boundary、connectivity、bidirectional consistency、logical order、metadata 和 reachability。

---

## 9. Iteration、Recursion 与 Complexity

### 9.1 Iteration 与 Recursion

Iteration 必须明确 traversal cursor、处理顺序和 precise stopping condition。Circular structure 如果错误地等待 `null`，可能出现 infinite loop。

正确 recursion 需要：

1. **Base Case（基本情况）**；
2. **Recursive Case（递归情况）**；
3. **Progress（每次更接近 base case）**；
4. **Return Propagation（将结果返回上一层）**。

一次前进一个 node 的 recursion 通常使用 $O(n)$ time 和 $O(n)$ call-stack space；对应 iteration 可能是 $O(n)$ time、$O(1)$ auxiliary space。

### 9.2 Big-O

令 $n$ 为当前 logical element 数量：

- $O(1)$：工作量不随 $n$ 增长；不等于“只有一行代码”。
- $O(n)$：需要 traversal 与 $n$ 成正比的 elements。
- 已知边界附近的局部操作可能为 $O(1)$；按 index 查找通常为 $O(n)$；完整转换或遍历通常为 $O(n)$。
- 除 time complexity 外，还要分析 object storage、temporary variables、recursive stack 与 removed objects 的 reachability。

---

## 10. Testing、Debugging 与 Style

### 10.1 Testing

CS 61B 使用 JUnit 的 `@Test` 和 Google Truth assertions：

```java
assertThat(actual).isEqualTo(expected);
```

采用 **Arrange–Act–Assert（AAA）**：建立 state、执行 behavior、验证 return value 和 resulting state。**Test-Driven Development（TDD）** 的循环是 Red → Green → Refactor：先确认 test 会失败，再实现 behavior，最后在 tests 保护下重构。

从 contract 推导 black-box scenarios：empty、single element、multiple elements、boundary、invalid input、repeated operations、mixed operation sequences 和 generic types。Coverage 只说明执行过哪些代码或 scenarios，不等于 assertions 足够强，也不构成 correctness proof。

### 10.2 Debugging

区分 compile-time error、runtime error 与 logic error。阅读 stack trace 时先找 exception type，再找第一条指向自己代码的 frame。使用 breakpoint、Step Over、Step Into 和 Java Visualizer 观察 object graph。

最有效的问题是：**哪一次 operation 之后，representation invariant 第一次不再成立？** 不要只在 `NullPointerException` 所在行机械加入 null check；错误状态往往更早已经产生。

### 10.3 Style 与限制

- 认真阅读 `Deque61B.java` 的全部 Javadocs。
- implementation 中只使用 specification 明确允许的 library data structures。
- 使用准确 method signature、`@Override`、generic types 和规范 naming/indentation。
- 提交前运行 local tests、debugger inspection 和 CS 61B style checker。
- 更完整的 style 复习见 [CS61B_Java_Style_Guide_Review.md](./CS61B_Java_Style_Guide_Review.md)。

---

## 11. 常见错误速查

- 认为 reference assignment 会 copy object。
- 把 Java object argument 误称为 pass-by-reference。
- 将 sentinel 当作 logical element，或把 circular traversal 写成等待 `null`。
- 双向结构只验证一个 traversal direction。
- Constructor 返回时 object 仍不满足 invariant。
- 为满足 $O(1)$ 的 operation 暗中进行完整 traversal。
- Recursive call 没有接近 base case。
- Logical removal 后仍保留不必要 references。
- Test 只执行 operations，没有 assertions 或不检查 intermediate state。
- 通过 public fields、无约束 setter 或 mutable getter 泄漏 representation。
- 混淆 `extends class`、`implements interface` 与 `interface extends interface`。
- 误以为 subpackage 自动拥有 parent package 的 package-private access。
- 将 helper method 设为 public，使调用者依赖 implementation detail。

---

## 12. 开工前 Checklist

- [ ] 能解释 ADT、API、implementation、representation 与 invariant。
- [ ] 能画 reference、aliasing 与 linked object graph。
- [ ] 能解释 Java pass-by-value、`null` 和 object reachability。
- [ ] 能区分 instance field、static field、local variable 与 parameter。
- [ ] 能解释 generic `T`、wrapper class、diamond operator 和 raw type。
- [ ] 能区分 static nested class 与 non-static inner class。
- [ ] 能比较 `extends`、`implements` 和 composition。
- [ ] 能解释 package-private、private method 与 representation exposure。
- [ ] 能分析常见 linked operations 的 time/space complexity。
- [ ] 能写 AAA tests，并用 debugger 找到 invariant 第一次失效的位置。

如果这些问题都能独立回答，就已经具备开始 Project 1A 的主要前置知识。编码前应再次完整阅读 specification 与 `Deque61B.java` Javadocs，并先用 object diagrams 推理结构状态。
