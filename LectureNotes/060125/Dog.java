public class Dog {
    public int weight;

    /* One integer constructor for Dog */
    public Dog(int w){
        weight = w;
    }

    public void makeNoise(){
        if (weight < 10){
            System.out.println("yipp");
        } else if (weight < 20){
            System.out.println("barrk");
        } else {
            System.out.println("wooolf");
        }

    }

    public static Dog maxDog(Dog d1, Dog d2){
        if (d1.weight > d2.weight){
            return d1;
        }else{
            return d2;
        }
    }

    public Dog minDog(Dog this, Dog d){
        if (this.weight < d.weight){
            return this;
        }else{
            return d;
        }
    }
}
