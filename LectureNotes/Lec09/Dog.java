import java.util.Comparator;

public class Dog implements Comparable<Dog>{
    public int weight;
    public String name;

    public Dog(int n, String m){
        weight = n;
        name = m;
    }

    public int compareTo(Dog d){
        return this.weight - d.weight;
    }


    public void bark(){
        System.out.println(name + " says barrrk");
    }

    private static class NameComparator implements Comparator<Dog>{
        public int compare(Dog a, Dog b){
            return a.name.compareTo(b.name);
        }
    }

    public static Comparator<Dog> getNameComparator(){
        return new NameComparator();
    }

}
