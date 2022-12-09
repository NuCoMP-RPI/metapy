import py4j.GatewayServer;

import com.google.inject.Inject;
import com.google.inject.Injector;

import java.io.IOException;

//import org.eclipse.emf.ecore.*;
import org.eclipse.emf.common.util.EList;
import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.ResourceSet;
import org.eclipse.xtext.resource.SaveOptions;
import org.eclipse.xtext.serializer.ISerializer;
import org.eclipse.xtext.xbase.lib.Exceptions;
import org.eclipse.xtext.testing.validation.ValidationTestHelper;
import org.eclipse.emf.ecore.util.EcoreUtil.Copier;
import org.eclipse.emf.ecore.util.EcoreUtil.EqualityHelper;
import org.eclipse.emf.ecore.util.EcoreUtil;
import org.eclipse.emf.ecore.EClass;

import fi.vtt.serpent.SerpentStandaloneSetup;
import fi.vtt.serpent.serpent.SerpentPackage;
import fi.vtt.serpent.serpent.SerpentFactory;

import gov.lanl.mcnp.McnpStandaloneSetup;
import gov.lanl.mcnp.mcnp.McnpPackage;
import gov.lanl.mcnp.mcnp.McnpFactory;

@SuppressWarnings("all")
public class EntryPoint {

	@Inject
	public ISerializer serializer;
	
	@Inject
	public ValidationTestHelper validator;
	
	public SerpentPackage ePackageSerpent = SerpentPackage.eINSTANCE;
    public McnpPackage ePackageMcnp = McnpPackage.eINSTANCE;
	
	public Copier copier = new Copier(true);
	
	public EqualityHelper equalityHelper = new EqualityHelper();
	
	public ResourceSet resourceSet;

	public SerpentFactory factorySerpent = SerpentFactory.eINSTANCE;
    public McnpFactory factoryMcnp = McnpFactory.eINSTANCE;

    public String getDocs(EClass e_class) {
        String doc = EcoreUtil.getDocumentation(e_class);

        return(doc);
    }

    public String printDeckSerpent(fi.vtt.serpent.serpent.Deck DECK) {
        // This really just seemed to hide useful error messages.
        // An invalid deck has no hope of serializing anyway.
        //this.validator.assertNoErrors(DECK);
        String serializedDeck = this.serializer.serialize(DECK, SaveOptions.newBuilder().format().getOptions());

        return(serializedDeck);
    }

    public String printDeckMcnp(gov.lanl.mcnp.mcnp.Deck DECK) {
        // This really just seemed to hide useful error messages.
        // An invalid deck has no hope of serializing anyway.
        //this.validator.assertNoErrors(DECK);
        String serializedDeck = this.serializer.serialize(DECK, SaveOptions.newBuilder().format().getOptions());

        return(serializedDeck);
    }

    // Reads a deck from a file
	public fi.vtt.serpent.serpent.Deck loadFileSerpent(String file) {
        try {
            Injector injector = new SerpentStandaloneSetup().createInjectorAndDoEMFRegistration();

            injector.injectMembers(this);
            ResourceSet resourceSet = injector.<ResourceSet>getInstance(ResourceSet.class);
            URI uri = URI.createURI(file);
            Resource xtextResource = resourceSet.getResource(uri, true);
            EcoreUtil.resolveAll(xtextResource);

            fi.vtt.serpent.serpent.Deck DECK = (fi.vtt.serpent.serpent.Deck) (xtextResource.getContents().get(0));
            this.validator.assertNoErrors(DECK);
            
            return(DECK);
        }
        catch (Throwable _e) {
            throw Exceptions.sneakyThrow(_e);
        }
    }

    // Reads a deck from a file
	public gov.lanl.mcnp.mcnp.Deck loadFileMcnp(String file) {
        try {
            Injector injector = new McnpStandaloneSetup().createInjectorAndDoEMFRegistration();
            injector.injectMembers(this);
            ResourceSet resourceSet = injector.<ResourceSet>getInstance(ResourceSet.class);
            URI uri = URI.createURI(file);
            Resource xtextResource = resourceSet.getResource(uri, true);
            EcoreUtil.resolveAll(xtextResource);

            gov.lanl.mcnp.mcnp.Deck DECK = (gov.lanl.mcnp.mcnp.Deck) (xtextResource.getContents().get(0));
            this.validator.assertNoErrors(DECK);
            
            return(DECK);
        }
        catch (Throwable _e) {
            throw Exceptions.sneakyThrow(_e);
        }
    }

    public fi.vtt.serpent.serpent.Deck deckResourceSerpent(fi.vtt.serpent.serpent.Deck deck, String filename) {
        Injector injector = new SerpentStandaloneSetup().createInjectorAndDoEMFRegistration();

        injector.injectMembers(this);
        ResourceSet resourceSet = injector.<ResourceSet>getInstance(ResourceSet.class);
        URI uri = URI.createURI(filename);
        Resource resource = resourceSet.createResource(uri);

        EList<EObject> _contents = resource.getContents();
        _contents.add(deck);
        Resource xtextResource = resourceSet.getResource(uri, true);
        EcoreUtil.resolveAll(xtextResource);
        return (deck);
    }

    public gov.lanl.mcnp.mcnp.Deck deckResourceMcnp(gov.lanl.mcnp.mcnp.Deck deck, String filename) {
        Injector injector = new McnpStandaloneSetup().createInjectorAndDoEMFRegistration();
        injector.injectMembers(this);
        ResourceSet resourceSet = injector.<ResourceSet>getInstance(ResourceSet.class);
        URI uri = URI.createURI(filename);
        Resource resource = resourceSet.createResource(uri);

        EList<EObject> _contents = resource.getContents();
        _contents.add(deck);
        Resource xtextResource = resourceSet.getResource(uri, true);
        EcoreUtil.resolveAll(xtextResource);
        return (deck);
    }

    public fi.vtt.serpent.serpent.Deck newSerpentDeck(String filename) {
        Injector injector = new SerpentStandaloneSetup().createInjectorAndDoEMFRegistration();

        injector.injectMembers(this);
        ResourceSet resourceSet = injector.<ResourceSet>getInstance(ResourceSet.class);
        URI uri = URI.createURI(filename);
        Resource resource = resourceSet.createResource(uri);

        fi.vtt.serpent.serpent.Deck DECK = factorySerpent.createDeck();

        EList<fi.vtt.serpent.serpent.Cell> cells = DECK.getCells();
        EList<fi.vtt.serpent.serpent.Surface> surfaces = DECK.getSurfaces();
        EList<fi.vtt.serpent.serpent.Material> materials = DECK.getMaterials();
        EList<fi.vtt.serpent.serpent.Card> data = DECK.getData();

        EList<EObject> _contents = resource.getContents();
        _contents.add(DECK);
        Resource xtextResource = resourceSet.getResource(uri, true);
        EcoreUtil.resolveAll(xtextResource);

        return(DECK);
    }
    
    // Creates an empty deck object with empty cell, surface, material, and data ELists.
    public gov.lanl.mcnp.mcnp.Deck newDeck(String filename) {
        McnpStandaloneSetup setup = new McnpStandaloneSetup();
        Injector injector = setup.createInjectorAndDoEMFRegistration();
        injector.injectMembers(this);
        ResourceSet resourceSet = injector.<ResourceSet>getInstance(ResourceSet.class);

        URI uri = URI.createURI(filename);
        Resource resource = resourceSet.createResource(uri);

        gov.lanl.mcnp.mcnp.Deck DECK = factoryMcnp.createDeck();
        gov.lanl.mcnp.mcnp.Surfaces SURFACES = factoryMcnp.createSurfaces();
        gov.lanl.mcnp.mcnp.Cells CELLS = factoryMcnp.createCells();
        gov.lanl.mcnp.mcnp.Data DATA = factoryMcnp.createData();

        EList<gov.lanl.mcnp.mcnp.Surface> surfs = SURFACES.getSurfaces();
        EList<gov.lanl.mcnp.mcnp.Cell> cells = CELLS.getCells();
        EList<gov.lanl.mcnp.mcnp.Material> mats = DATA.getMaterials();
        EList<gov.lanl.mcnp.mcnp.Setting> settings = DATA.getSettings();

        DECK.setCells(CELLS);
        DECK.setSurfaces(SURFACES);
        DECK.setData(DATA);
        EList<EObject> _contents = resource.getContents();
        _contents.add(DECK);
        Resource xtextResource = resourceSet.getResource(uri, true);
        EcoreUtil.resolveAll(xtextResource);

        return(DECK);
    }

    public static void main(String[] args) {
        GatewayServer gatewayServer = new GatewayServer(new EntryPoint());
        gatewayServer.start();
        System.out.println("Gateway Server Started");
    }

    public void startupComplete() {
        System.out.println("Gateway Server Started");
    }

}
