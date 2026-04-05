public class TYIterator extends OHIterator{
    public TYIterator(OHRequest queue) {
        super(queue);
    }

    @Override
    public OHRequest next(){
        OHRequest result = super.next();
        if (curr != null && curr.description.contains("thank u")){
            result = super.next();
        }
        return result;

    }

}
