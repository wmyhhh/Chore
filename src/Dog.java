public class Dog {
    public int weightInPounds;  // instance variable
    /** One integer constructor of Dog */
    public Dog(int w){      // constructor
        weightInPounds = w;
    }
    public void makeNoise() {   // non-static method a.k.a instance method
        if (weightInPounds < 10) {
            System.out.println("yip!");
        }else if (weightInPounds < 30) {
            System.out.println("bark!");
        }else {
            System.out.println("woof!");
        }
    }
    public static String binomen = "Canis familiaris";
    public static Dog maxDog(Dog d1, Dog d2){
        if (d1.weightInPounds > d2.weightInPounds) {
            return d1;
        }
        return d2;
    }
    public Dog compareDog(Dog d2){
        if (this.weightInPounds > d2.weightInPounds) {
            return this;
        }
        return d2;
    }
}
