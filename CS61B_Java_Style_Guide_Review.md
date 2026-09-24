# CS 61B Java Style Guide 复习笔记

> 依据：[CS 61B Spring 2024 Style Guide](https://sp24.datastructur.es/resources/guides/style/)
>
> 这份笔记既覆盖原文的全部规则，也重点整理了我们讨论过的 variable、field、constructor、modifier、inheritance、`equals`、`hashCode`、shadowing 等概念。课程的 automated style checker（自动风格检查器）才是作业验收时的直接标准；提交前应保存或重新编译文件，再运行 IntelliJ 的 **Check Style**。

---

## 1. 先建立整体概念

### 1.1 Class、object 与 instance

`class` 是一种 type（类型）的定义，描述对象包含什么 data 和 behavior；`object` 是程序运行时实际存在的数据实体；`instance` 强调某个 object 是由某个 class instantiate（实例化）得到的。

```java
public class Student {
    private String _name;
}
```

上面只是 declare（声明）了 `Student` class，还没有创建 Student object。下面的 `new` expression 才会 instantiate 一个 instance：

```java
Student alice = new Student("Alice");
```

其中：

- 第一个 `Student` 是 variable `alice` 的 declared type（声明类型）。
- `alice` 是保存 object reference（对象引用）的 variable。
- `new Student("Alice")` 创建并初始化一个 `Student` instance。
- `Student("Alice")` 调用 `Student` constructor（构造器）。

一个 class 可以产生多个彼此独立的 instance：

```java
Student alice = new Student("Alice");
Student bob = new Student("Bob");
```

### 1.2 Constructor 不是普通 method

Constructor 用于初始化刚创建的 object：

```java
public Student(String studentName) {
    String normalizedName = studentName.trim();
    _name = normalizedName;
    _studentCount++;
}
```

Constructor 有两个识别特征：

1. 名字与 class 名完全相同。
2. 没有 return type，连 `void` 也不能写。

```java
public Student(String studentName) { }
//     ^ constructor

public void setName(String studentName) { }
//          ^ ordinary method
```

若写成 `public void Student(...)`，它会成为一个名字恰好叫 `Student` 的 ordinary method，而不是 constructor。

执行 `new Student("  Alice  ")` 时，可以概念化为：

1. 为新的 `Student` object 分配空间。
2. Instance fields 先获得默认值。
3. 执行 field initializers。
4. 调用 matching constructor。
5. Constructor 初始化当前 object。
6. 返回该 object 的 reference。

### 1.3 Parameter、local variable、instance field 与 static field

```java
public class Student {
    private static int _studentCount = 0;
    private String _name;

    public Student(String studentName) {
        String normalizedName = studentName.trim();
        _name = normalizedName;
        _studentCount++;
    }
}
```

| Identifier | Formal category | 属于谁 | Scope / lifetime 的核心含义 |
|---|---|---|---|
| `studentName` | parameter | 本次 constructor invocation | 只在 constructor body 中可见 |
| `normalizedName` | local variable | 本次 constructor invocation | 从 declaration 到所在 block 结束 |
| `_name` | instance variable / instance field | 当前 `Student` instance | 每个 instance 有自己的一份 |
| `_studentCount` | class variable / static field | `Student` class | 所有 Student instances 共享一份 |

数据流为：

```text
argument "  Alice  "
        ↓
parameter studentName
        ↓  trim()
local variable normalizedName = "Alice"
        ↓
instance field this._name = "Alice"
```

`_name = normalizedName` 等价于 `this._name = normalizedName`；`this` 表示当前正在初始化的 instance。`_studentCount++` 则可以更明确地写成 `Student._studentCount++`，因为它属于 class 而不是某个 instance。

Instance field 会获得默认值，例如 `int` 为 `0`、`boolean` 为 `false`、reference 为 `null`。Local variable 没有自动默认值，读取前必须 definite assignment（明确赋值）。

### 1.4 Method、type、type parameter 与 package

- `method` 表示 class 中定义的 behavior，例如 `getName()`、`calculateScore()`。
- `type` 描述一个值所属的类型，例如 `int`、`String`、`Student`。
- `class` 是定义 reference type 的主要机制之一。
- `type parameter` 是 generic declaration（泛型声明）中的类型占位符，例如 `class Box<T>` 中的 `T`。
- `package` 用于组织相关类型并避免 naming collision，例如 `edu.berkeley.cs61b`。

---

## 2. Names：命名规则

### 2.1 Static final constants 使用全大写

```java
public static final int MAX_SIZE = 100;
private static final String DEFAULT_NAME = "Unknown";
```

多个单词用 underscore 连接。`static` 表示属于 class，`final` 表示 variable 不能重新赋值。注意：一个 `static final` reference 不能改为指向另一个 object，但被引用的 mutable object 仍可能被修改。

```java
private static final List<String> NAMES = new ArrayList<>();

NAMES.add("Alice");           // 可以修改 List 的内容
// NAMES = new ArrayList<>(); // 不可以重新赋值 NAMES
```

### 2.2 Parameter、local variable 与 method 从小写开始

```java
int currentSize;
String studentName;
void calculateScore() { }
```

它们也可以是单个大写字母；这通常出现在简短的数学变量或 generic-related context 中，但 method 一般仍采用 lower camel case（小驼峰形式）。

### 2.3 Type 与 type parameter 从大写开始

```java
Student
CourseRecord
BinarySearchTree
T
E
K
V
```

常见单字母 type parameter：`T` 表示 Type，`E` 表示 Element，`K` 表示 Key，`V` 表示 Value。

### 2.4 Package 从小写开始

```java
package edu.berkeley.cs61b;
```

实践中 package name 通常全部小写。

### 2.5 Instance field 和 non-final static field

它们必须以小写字母或 `_` 开始：

```java
private int _size;               // instance field
private static int objectCount;  // non-final static field
```

本课程特别推荐 `_fieldName`，因为这样可以避免 parameter 或 local variable shadow field。

---

## 3. Whitespace 与 indentation

### 3.1 文件和 indentation

- 每个文件必须以 newline 结尾。
- 禁止 horizontal tab character；只用 space。
- 每一级 block 使用 4 spaces indentation。
- Continued line（续行）也增加一个基本 indentation step。
- `switch` 中的 `case` label 要比 `switch` 多缩进一级。

```java
switch (operation) {
    case '+':
        addOperands(x, y);
        break;
    default:
        reportError();
}
```

### 3.2 不应出现 space 的位置

```java
List<Integer> values; // 不是 List <Integer> 或 List< Integer >
!ready;               // 不是 ! ready
++index;              // 不是 ++ index
index++;              // 不是 index ++
call(value);          // 不是 call( value )
object.method();      // 不是 object. method()
```

更完整地说：prefix operators `!`、`--`、`++`、unary `-`、unary `+` 后不能插入 space；`;` 和 suffix `--`、`++` 前不能插入 space；`(` 后、`)` 前以及 `.` 后也不能插入 space。

`methodName` 和 call 的 `(` 之间也不能有 space：

```java
calculate(value);  // correct
// calculate (value);  // incorrect
```

Long call 因 line-length limit 必须换行时，method name 和 `(` 之间可以插入 newline，再用 spaces 完成 indentation。

### 3.3 应出现 space 的位置

```java
int x = 1;
int y = x + 2;
boolean larger = x >= y;
String text = (String) value;
int absolute = x > 0 ? x : -x;
```

- `;`、`,` 和 type cast 后需要 space。
- Binary operator、comparison operator 和 assignment operator 两边需要 space。
- Ternary conditional operator 的 `?`、`:` 两边需要 space。
- `if`、`for`、`while`、`catch`、`return` 等 keyword 后按语法需要保留 space。

Long statement 换行时，通常在 operator 之前断行：

```java
int result = initialValue
    + width * height
    + offset;
```

---

## 4. Braces：花括号规则

所有 `if`、`while`、`do`、`for` body 都必须使用 braces，即使只有一个 statement：

```java
if (ready) {
    run();
}
```

不要写：

```java
if (ready)
    run();
```

Opening brace 通常放在 header 行末；`else`、`catch`、`finally` 与前一个 closing brace 放在同一行：

```java
try {
    load();
} catch (IOException exc) {
    report(exc);
} finally {
    close();
}
```

若 line-length limit 迫使 opening brace 移到下一行，则 brace 单独占一行且不额外 indent。

这样能避免后来增加 statement 时意外改变 control flow，也保持 block boundary 清晰。

---

## 5. Comments 与 Javadoc

Method 应有 Javadoc，解释 behavior、parameters 和 return value。第一句话必须是完整句子：以大写字母开头，以 period 结尾。

```java
/**
 * Returns the area of this rectangle.
 *
 * @return the product of the width and height.
 */
public double area() {
    return _width * _height;
}
```

有 parameter 时可使用 `@param`：

```java
/**
 * Changes the width of this rectangle.
 *
 * @param width the new nonnegative width.
 */
public void setWidth(double width) {
    _width = width;
}
```

Non-`void` method 的 Javadoc 必须通过 `@return`，或在正常句子中使用 `return`、`returning`、`returns` 说明 return value。

---

## 6. Imports 与 array declaration

### 6.1 Imports

- 不要重复 import 同一个 class 或 static member。
- 不要保留 unused import。

### 6.2 Array brackets 跟 element type

```java
String[] names; // correct
// String names[]; // incorrect style
```

两种形式在 Java 中都可能编译，但课程规定 `[]` 紧跟 element type。

---

## 7. Modifier：含义与顺序

Modifier 应按以下 canonical order（规范顺序）书写：

```text
public / protected / private
→ abstract / static
→ final / transient / volatile
→ synchronized
→ native
→ strictfp
```

常见正确示例：

```java
public abstract class Shape { }
public static final int MAX_SIZE = 100;
protected final synchronized void update() { }
```

Java compiler 有时接受其他顺序，但 style checker 要求统一。不是所有 modifier 都适用于所有 declaration，也不是要求把整条列表全部写上。

| Modifier | Formal meaning | 常见用途 |
|---|---|---|
| `public` | public access | 任意可见位置可访问 |
| `protected` | protected access | 同 package 与 subclass 可访问 |
| `private` | private access | 当前 class 内可访问 |
| `abstract` | incomplete implementation | class 或 method 留待 subclass 实现 |
| `static` | class-level membership | 成员属于 class 而非 instance |
| `final` | prohibited reassignment/override/extension | 依修饰对象分别禁止重新赋值、override 或继承 |
| `transient` | excluded from ordinary serialization | field 序列化控制 |
| `volatile` | cross-thread visibility | 保证读取到较新的写入，但不自动保证 compound operation 的 atomicity |
| `synchronized` | monitor-based synchronization | method 调用获得对应 monitor lock（监视器锁） |
| `native` | non-Java implementation | 常结合 JNI（Java Native Interface） |
| `strictfp` | strict floating-point evaluation | 统一浮点计算行为；现代 Java 中较少需要 |

### 7.1 不写 redundant modifier

Redundant modifier 是 Java language 已经隐含、显式写出不增加语义的信息。

#### Interface / annotation methods

普通 interface method 隐含 `public abstract`：

```java
public interface Shape {
    double area();
}
```

不要写 `public abstract double area();`。现代 interface 还可能有 `default`、`static` 或 `private` method；这些改变 method category 的 modifier 不是冗余的。

#### Interface / annotation fields

Interface field 隐含 `public static final`：

```java
public interface Configuration {
    int MAX_SIZE = 100;
}
```

#### Final class methods

`final class` 无法产生 subclass，因此其中的方法已经不可能被 subclass override；不要再给它们加 `final`。

#### Nested interface

Member interface 隐含 `static`：

```java
public class Container {
    public interface Listener {
        void changed();
    }
}
```

---

## 8. `final class`、inheritance 与 override

### 8.1 什么是 inheritance

```java
public class Person {
    public void introduce() {
        System.out.println("I am a person.");
    }
}

public class Student extends Person {
    public void study() {
        System.out.println("I am studying.");
    }
}
```

`Student extends Person` 表示 `Student` 是 subclass，`Person` 是 superclass。Student instance 可以使用继承到的 accessible behavior。

### 8.2 `final class` 的准确方向

```java
public final class Student extends Person {
}
```

这表示：

- `Student` 自己可以继承 `Person`。
- 其他 class 不能再写 `extends Student`。

```java
// Compile-time error: Student is final.
public class GraduateStudent extends Student {
}
```

`final class` 仍然可以正常 instantiate，也不自动代表它的 objects 是 immutable。

### 8.3 `final` 在不同位置的区别

- `final class`：不能被其他 class extend。
- `final method`：subclass 不能 override 该 method。
- `final variable`：variable 不能重新赋值；若它保存 reference，object 内容未必不可修改。

### 8.4 为什么使用 final class

- 明确 class 不支持 extension。
- 防止 subclass override 关键 behavior 并破坏 invariant。
- Utility class 没有 instance/subclass 的设计需求。
- 简化 `equals` 的 type relationship，避免 superclass 与 subclass equality 破坏 symmetry。

---

## 9. Field visibility 与 encapsulation

只有 `static final` class field 才可以是 `public`：

```java
public static final int DEFAULT_CAPACITY = 16;
```

其他 fields 必须是 `private` 或 `protected`：

```java
private int _size;
protected Node _root;
private static int _objectCount;
```

以下不符合规则：

```java
public int size;
public static int objectCount;
```

原因是 encapsulation（封装）：外部代码不应绕过 method 直接破坏 object invariant。公开 `static final` field 只是“允许”，不是“必须”；常量也可以是 `private`。若公开的 `static final` field 指向 mutable object，外部仍可能修改其内容，因此公开常量最好采用 primitive value、`String` 或其他 immutable object。

这条规则也适用于 nested class 内部的 fields；它并不是说 nested class 本身不能 `public`。

---

## 10. Utility class 与 constructor

只有 static fields 和 static methods 的 class 是 utility class，不需要 instance：

```java
public final class MathUtils {
    public static final double EPSILON = 0.000001;

    private MathUtils() {
        throw new AssertionError("Utility class must not be instantiated.");
    }

    public static int square(int value) {
        return value * value;
    }
}
```

若完全不 declare constructor，compiler 会生成 default constructor，使无意义的 `new MathUtils()` 成为可能。因此 utility class 要显式使用 private constructor。

若一个 class 的所有 constructors 都是 `private`，课程规则还要求把 class declare 为 `final`。这明确表达“不能正常从外部 instantiate，也不允许 subclass”的设计意图。

---

## 11. Exception handling

不要笼统 catch `Exception`、`Error`，也不要用过宽的 catch 隐藏 programming bug：

```java
try {
    readFile();
} catch (IOException exc) {
    reportFileError(exc);
}
```

如果多个具体 exception 采用同一种 recovery，可以使用 multi-catch：

```java
try {
    loadConfiguration();
} catch (IOException | ParseException exc) {
    useDefaultConfiguration();
}
```

`Error` 通常表示 JVM（Java Virtual Machine）或 runtime environment 的严重问题，例如 `OutOfMemoryError` 和 `StackOverflowError`，普通业务代码通常无法可靠恢复。`RuntimeException` 常表示 programming error，但特定且可恢复的 subtype，例如用户输入导致的 `NumberFormatException`，可以在明确场景中处理。

> 原文写的是 `RuntimeError`。Java standard library 中常见的 broad runtime type 是 `RuntimeException`，没有通常所指的标准 `RuntimeError` class；这很可能是原文笔误。无论如何，本规则的核心是不要 catch 过宽、自己无法正确处理的 throwable category。

Control statement 不应使用 empty block。课程允许的例外是确实需要忽略某个 exception 时，catch body 只放规定形式的 comment：

```java
try {
    closeResource();
} catch (IOException exc) {
    /* Ignore IOException. */
}
```

不要使用空 catch 吞掉 exception。

---

## 12. `equals` 与 `hashCode`

### 12.1 Reference equality 与 logical equality

```java
Student first = new Student("1001", "Alice");
Student second = new Student("1001", "Alice");
```

`first == second` 比较 references 是否指向同一个 object，通常为 `false`。`first.equals(second)` 可以根据业务定义判断 logical equality，例如“student ID 相同就表示同一名学生”。

Every class 最终继承 `Object.equals(Object)` 和 `Object.hashCode()`。Override 表示 class 提供同 signature 的新 implementation；`@Override` 让 compiler 检查 signature 是否正确。

### 12.2 Equality contract

一个正常的 `equals` implementation 应满足：

- Reflexive：`x.equals(x)` 为 `true`。
- Symmetric：`x.equals(y)` 与 `y.equals(x)` 结果一致。
- Transitive：若 `x` 等于 `y` 且 `y` 等于 `z`，则 `x` 等于 `z`。
- Consistent：参与比较的数据不变时，多次调用结果一致。
- Non-null：`x.equals(null)` 为 `false`。

### 12.3 Hash code contract

最重要的方向是：

```text
a.equals(b) == true
        必须推出
a.hashCode() == b.hashCode()
```

反方向不成立：相同 hash code 不保证 objects 相等。不同 objects 得到相同 hash code 称为 hash collision（哈希碰撞），是合法且不可完全避免的。

### 12.4 HashSet / HashMap 的查找逻辑

可以把 hash-based collection 概念化为多个 buckets：

```text
object
  ↓ hashCode()
定位可能的 bucket
  ↓ equals()
在 bucket 内确认 logical equality
```

`hashCode` 用于快速缩小候选范围，`equals` 负责最终确认。若两个 equal objects 返回不同 hash codes，collection 可能去错误的 bucket，甚至根本不调用它们之间的 `equals`。

例如：

```java
Set<Student> students = new HashSet<>();
Student first = new Student("1001", "Alice");
Student second = new Student("1001", "Alicia");

students.add(first);
boolean present = students.contains(second);
```

如果 logical identity 只由 student ID 决定，那么 `present` 应为 `true`。这要求 `first` 与 `second` 不但 `equals` 为 `true`，还必须具有相同 hash code。

### 12.5 正确实现

```java
import java.util.Objects;

public final class Student {
    private final String _studentId;
    private String _name;

    public Student(String studentId, String name) {
        _studentId = studentId;
        _name = name;
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (!(other instanceof Student)) {
            return false;
        }

        Student otherStudent = (Student) other;
        return Objects.equals(_studentId, otherStudent._studentId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(_studentId);
    }
}
```

Line-by-line logic：

1. `this == other` 快速处理同一个 object。
2. `instanceof Student` 检查 type；对 `null` 也会得到 `false`。
3. Cast 后取得另一个 Student。
4. 使用 `_studentId` 判断 logical equality。
5. `hashCode` 也只使用 `_studentId`。

核心规则是：`equals` 使用哪些 identity fields，`hashCode` 就必须基于相同的 equality definition。如果 `equals` 只比较 `_studentId`，就不能让 `hashCode` 额外依赖 `_name`，否则同 ID、不同 name 的两个 equal objects 可能产生不同 hash codes。

### 12.6 为什么 identity field 最好 immutable

Object 放入 `HashSet` 或作为 `HashMap` key 后，如果参与 `hashCode` 的 field 改变，object 的新 hash code 可能指向另一个 bucket，而它实际上仍存放在旧 bucket，导致 `contains` 或 `get` 失败。

因此 identity field 常 declare 为 `final`：

```java
private final String _studentId;
```

### 12.7 Final class 对 equals 的帮助

若 class 可以被 subclass，父类可能只比较 student ID，而 subclass 还想比较额外 field，容易破坏 symmetry 或 transitivity。`final class Student` 排除了 subclass，使 equality domain 更简单；这不是实现正确 `equals` 的唯一方法，但能减少 inheritance 带来的复杂性。

---

## 13. Shadowing 与 field name

Local variable 和 parameter 不能 shadow field：

```java
public class Rectangle {
    private double width;

    public void setWidth(double width) {
        width = width; // 两边都解析为 parameter
    }
}
```

虽然普通 Java style 常写 `this.width = width`，本课程仍认为 parameter `width` shadow 了 field `width`。推荐 field 加 `_`：

```java
public class Rectangle {
    private double _width;

    public double getWidth() {
        return _width;
    }

    public void setWidth(double width) {
        _width = width;
    }
}
```

也不要在 method 内重新 declare 同名 local variable：

```java
private int _count;

public void reset() {
    int _count = 0; // incorrect: local variable shadows field
}
```

这里的 shadowing 是 lexical name resolution（词法名称解析）问题；hiding 更常描述 subclass 中的同名 static member。课程把二者放在同一条规则中，核心目的都是避免依靠 scope 猜测 identifier 指向哪个 declaration。

---

## 14. 避免 error-prone constructs

### 14.1 不使用 nested assignment

Assignment 在 Java 中也是 expression，因此下面语法成立但不符合规则：

```java
if ((value = next()) != null) {
    process(value);
}
```

应把 side effect（副作用）单独写成 statement：

```java
value = next();
if (value != null) {
    process(value);
}
```

同理，避免 `a = b = 0`、`print(value = calculate())` 等把 assignment 嵌入其他 expression 的写法。拆分后 execution order、debugging breakpoint 和错误定位都更清楚。

### 14.2 Boolean expression 直接使用

```java
if (ready) { }
if (!ready) { }
```

不要写：

```java
if (ready == true) { }
if (ready == false) { }
```

同样，不要把一个 condition 重新包装为 `true`/`false`：

```java
return condition;
```

不要写：

```java
if (condition) {
    return true;
} else {
    return false;
}
```

### 14.3 `switch` 必须有 `default`

```java
switch (command) {
    case "start":
        start();
        break;
    case "stop":
        stop();
        break;
    default:
        reportUnknownCommand();
        break;
}
```

每个 arm 必须以 `break` 结束；若有意 fall-through，则放置精确 comment：

```java
case 1:
    prepare();
    /* fall through */
case 2:
    execute();
    break;
```

### 14.4 String 内容比较使用 equals

```java
if (value.equals("something")) {
    // ...
}
```

不要写：

```java
if (value == "something") {
    // ...
}
```

`==` 比较 reference identity，不是一般意义上的 String content。若 `value` 可能为 `null`，可以把已知 non-null literal 放在前面：

```java
if ("something".equals(value)) {
    // ...
}
```

### 14.5 避免 magic numbers

Magic number 是缺少名称和语义说明的数值 literal：

```java
if (_size > 100) {
    // 100 的含义不明确
}
```

应引入 symbolic constant：

```java
private static final int MAX_SIZE = 100;

if (_size > MAX_SIZE) {
    // ...
}
```

原 guide 将 `-1`、`0` 到 `9`、`0.25`、`0.5` 列为允许直接出现的常用 numerical exceptions，但即使数值很小，只要其 domain meaning 不直观，使用 named constant 仍可能更清晰。

---

## 15. Size limits

| Item | Limit |
|---|---:|
| 单个 source file | 最多 2000 lines |
| 单行 | 最多 120 characters |
| 单个 method | 最多 80 lines |
| 单个 method parameters | 最多 8 个 |
| Outer class | 每个文件恰好 1 个；允许 nested classes |

这些限制推动 decomposition（分解）：过长 method 通常应提取 helper method，过多 parameters 可能提示相关数据应组合成 object，过大 class/file 可能承担了过多 responsibility。

---

## 16. 综合示例

```java
import java.util.Objects;

/** Represents a student identified by an immutable student ID. */
public final class Student {
    public static final int DEFAULT_MAX_COURSES = 4;

    private static int _studentCount = 0;
    private final String _studentId;
    private String _name;

    /**
     * Creates a student with the specified ID and name.
     *
     * @param studentId the immutable identifier of the student.
     * @param name the initial display name.
     */
    public Student(String studentId, String name) {
        String normalizedName = name.trim();
        _studentId = studentId;
        _name = normalizedName;
        _studentCount++;
    }

    /**
     * Returns the display name of this student.
     *
     * @return the current display name.
     */
    public String getName() {
        return _name;
    }

    /**
     * Changes the display name of this student.
     *
     * @param name the new display name.
     */
    public void setName(String name) {
        _name = name.trim();
    }

    /**
     * Returns whether another object represents the same student.
     *
     * @param other the object to compare with this student.
     * @return true if both objects have the same student ID.
     */
    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (!(other instanceof Student)) {
            return false;
        }

        Student otherStudent = (Student) other;
        return Objects.equals(_studentId, otherStudent._studentId);
    }

    /**
     * Returns a hash code based on the immutable student ID.
     *
     * @return a hash code consistent with equals.
     */
    @Override
    public int hashCode() {
        return Objects.hash(_studentId);
    }
}
```

这个例子集中体现了：

- Class/type 从大写开始，methods、parameters、local variables 从小写开始。
- Constant 使用 `UPPER_SNAKE_CASE`。
- Fields 使用 `_` 前缀，避免 parameter shadowing。
- Modifier 顺序正确。
- Mutable fields 不公开。
- Constructor 初始化 instance fields，并更新 shared static field。
- `final class` 禁止 subclass。
- `equals` 与 `hashCode` 基于相同 immutable identity field。
- Braces、indentation、spacing 和 Javadoc 符合 guide 的主要规则。

---

## 17. 提交前 checklist

### Formatting

- [ ] 文件末尾有 newline，没有 tab。
- [ ] 每层 indentation 是 4 spaces。
- [ ] Operators、casts、commas 和 parentheses 周围 spacing 正确。
- [ ] 所有 control statement 都有 braces。
- [ ] `else`、`catch`、`finally` 与前一个 `}` 同行。
- [ ] 每行不超过 120 characters。

### Naming and declarations

- [ ] Constants 使用全大写和 underscore。
- [ ] Methods、parameters、local variables 从小写开始。
- [ ] Types 和 type parameters 从大写开始。
- [ ] Package 从小写开始。
- [ ] Fields 从小写或 `_` 开始。
- [ ] Array 写成 `Type[] name`。
- [ ] Modifier 顺序正确，没有 redundant modifier。
- [ ] 没有 duplicate / unused imports。

### Design and correctness

- [ ] Mutable fields 都是 `private` 或 `protected`。
- [ ] Utility class 有 private constructor，并 declare 为 `final`。
- [ ] `equals` 和 `hashCode` 总是一起 override。
- [ ] 两者使用一致的 equality fields。
- [ ] Parameter / local variable 没有 shadow field。
- [ ] 没有 broad catch、empty control block 或 nested assignment。
- [ ] Boolean expression 没有与 `true` / `false` 多余比较。
- [ ] String content 没有使用 `==` 比较。
- [ ] `switch` 有 `default`，每个 arm 有 `break` 或 `/* fall through */`。
- [ ] Magic number 已替换为 meaningful constant。
- [ ] File、method 和 parameter count 没有超过 limits。
- [ ] 已保存或重新编译，然后运行 IntelliJ **Check Style**。

---

## 18. 快速自测

1. `Student alice = new Student("Alice")` 中两个 `Student` 分别表示什么？
2. Constructor 与 ordinary method 在 declaration 上最明显的区别是什么？
3. Parameter、local variable、instance field、static field 分别属于什么 scope？
4. 为什么本课程偏好 `_width = width`，而不是 `this.width = width`？
5. `final class Student extends Person` 禁止的是哪一个继承方向？
6. 为什么 `static final List<String>` 不一定是真正 immutable 的常量？
7. `equals` 为 `true` 时，`hashCode` 必须满足什么关系？反方向是否成立？
8. HashSet 为什么先调用 `hashCode`，之后才可能调用 `equals`？
9. 为什么放进 HashMap 的 key 不应修改参与 `hashCode` 的 field？
10. 为什么 `value == "hello"` 不是一般的 String content comparison？
11. 为什么 utility class 需要显式 private constructor？
12. 为什么 nested assignment 会提高误读与 debugging 的难度？

如果能不看正文准确回答这些问题，就已经掌握了本轮讨论中最核心的知识点。
