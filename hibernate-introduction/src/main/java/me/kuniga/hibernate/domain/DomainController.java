package me.kuniga.hibernate.domain;

import java.util.List;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;


public class DomainController {
	
	private static final EntityManagerFactory entityManagerFactory = Persistence.createEntityManagerFactory("me.kuniga.hibernate.jpa");

	public static void addEntity(GenericEntity entity){

		EntityManager entityManager = entityManagerFactory.createEntityManager();
		entityManager.getTransaction().begin();
		entityManager.persist(entity);
		entityManager.getTransaction().commit();
		entityManager.close();		
	}
	
	public static List<GenericEntity> getEntityList(){
		
		EntityManager entityManager = entityManagerFactory.createEntityManager();
		entityManager.getTransaction().begin();
		List<GenericEntity> entityList = entityManager.createQuery( "from GenericEntity", GenericEntity.class ).getResultList();			
		entityManager.getTransaction().commit();
		entityManager.close();
		return entityList;
	}
	
}
