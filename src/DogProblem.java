public class DogProblem {
    public static Dog[] BiggerThanFourNeighbours(Dog[] dogs){
        Dog[] returnDogs = new Dog[dogs.length];
        int cnt = 0;
        for (int i = 0; i < dogs.length; i ++){
            if (isBiggest(dogs,i)){
                returnDogs[cnt] = dogs[i];
                cnt = cnt + 1;
            }
        }
        // returnDogs = arrayWithoutNull(returnDogs, cnt);
        return returnDogs;
    }
    public static boolean isBiggest(Dog[] dogs, int i){
        boolean isBig = true;
        for (int j = -2; j <= 2; j ++){
            int compareIndex = i + j;
            if (j == 0){
                continue;
            }
            if (validIndex(dogs, compareIndex)){
                if(dogs[compareIndex].weightInPounds >= dogs[i].weightInPounds){
                    isBig = false;
                }
            }
        }
        return isBig;
    }
    public static boolean validIndex(Dog[] dogs, int i){
        if (i < 0){
            return false;
        }
        if (i >= dogs.length){
            return false;
        }
        return true;
    }
    public static void main(String[] args){
        Dog[] dogs = new Dog[]{
                new Dog(10),
                new Dog(15),
                new Dog(20),
                new Dog(10),
                new Dog(5),
                new Dog(12),
                new Dog(10),
                new Dog(8),
                new Dog(10)

        };
        Dog[] result = BiggerThanFourNeighbours(dogs);

        for (int k = 0; k < result.length; k ++){
            System.out.println(result[k].weightInPounds + " ");
        }
    }
}

