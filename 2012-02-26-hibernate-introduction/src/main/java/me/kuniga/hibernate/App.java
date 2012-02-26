package me.kuniga.hibernate;

import java.util.Date;
import java.util.List;

import me.kuniga.hibernate.domain.DomainController;
import me.kuniga.hibernate.domain.GenericEntity;


/**
 * Class to test the hibernate persistence (read/write) 
 *
 */
public class App 
{
    public static void main( String[] args )
    {

    	// Create a generic entity
        GenericEntity entity = new GenericEntity();
        entity.setName("foo");
        
        Date d = new Date(System.currentTimeMillis());
        entity.setDate(d);
                        
        DomainController.addEntity(entity);
        
        // Le entidades da base de dados
        List<GenericEntity> entityList = DomainController.getEntityList();
    	System.out.println("Lista de entidades");
        for(GenericEntity entityItem : entityList)
        	System.out.println(entity.getId() + " " + entityItem.getName() + " " + entityItem.getDate());
        
    	System.out.println("Teste finalizado");

    }
}
