import numpy as np
from matplotlib.ticker import FuncFormatter

def get_data(t, i):
    return []

def to_percent(y, position):
    return f"{round(y * 100, 3)}%"

def graphPrices_Log(t, plt):
    "Prices (Logarithmic)"
    food = get_data(t, 'Global Food Price')
    salt = get_data(t, 'Global Salt Price')
    fiber = get_data(t, 'Global Fiber Price')
    fuel = get_data(t, 'Global Fuel Price')
    raw = get_data(t, 'Global Raw Material Price')
    delicacies = get_data(t, 'Global Delicacies Price')
    exotic = get_data(t, 'Global Exotics Price')
    consumer = get_data(t, 'Global Consumer Product Price')
    military = get_data(t, 'Global Military Product Price')
    naval = get_data(t, 'Global Naval Product Price')
    industrial = get_data(t, 'Global Industrial Product Price')
    luxury = get_data(t, 'Global Luxury Product Price')
    knowledge = get_data(t, 'Global Knowledge Price')
    itr = range(1, len(food) + 1)

    plt.plot(itr, food, 'tab:blue', label="Food")
    plt.plot(itr, salt, 'tab:orange', label="Salt")
    plt.plot(itr, fiber, 'tab:green', label="Fiber")
    plt.plot(itr, fuel, 'tab:red', label="Fuel")
    plt.plot(itr, raw, 'tab:purple', label="Raw")
    plt.plot(itr, delicacies, label="Delicacies")
    plt.plot(itr, exotic, 'tab:brown', label="Exotic")
    plt.plot(itr, consumer, 'tab:pink', label="Consumer")
    plt.plot(itr, military, 'tab:gray', label="Military")
    plt.plot(itr, naval, 'tab:olive', label="Naval")
    plt.plot(itr, industrial, 'tab:cyan', label="Industrial")
    plt.plot(itr, luxury, 'rosybrown', label="Luxury")
    plt.plot(itr, knowledge, 'teal', label="Knowledge")
    plt.set_yscale('log')

def graphPrices(t, plt):
    "Prices"
    food = get_data(t, 'Global Food Price')
    salt = get_data(t, 'Global Salt Price')
    fiber = get_data(t, 'Global Fiber Price')
    fuel = get_data(t, 'Global Fuel Price')
    raw = get_data(t, 'Global Raw Material Price')
    delicacies = get_data(t, 'Global Delicacies Price')
    exotic = get_data(t, 'Global Exotics Price')
    consumer = get_data(t, 'Global Consumer Product Price')
    military = get_data(t, 'Global Military Product Price')
    naval = get_data(t, 'Global Naval Product Price')
    industrial = get_data(t, 'Global Industrial Product Price')
    luxury = get_data(t, 'Global Luxury Product Price')
    knowledge = get_data(t, 'Global Knowledge Price')
    itr = range(1, len(food) + 1)

    plt.plot(itr, food, label="Food")
    plt.plot(itr, salt, label="Salt")
    plt.plot(itr, fiber, label="Fiber")
    plt.plot(itr, fuel, label="Fuel")
    plt.plot(itr, raw, label="Raw")
    plt.plot(itr, delicacies, label="Delicacies")
    plt.plot(itr, exotic, label="Exotics")
    plt.plot(itr, consumer, label="Consumer")
    plt.plot(itr, military, label="Military")
    plt.plot(itr, naval, label="Naval")
    plt.plot(itr, industrial, label="Industrial")
    plt.plot(itr, luxury, label="Luxury")
    plt.plot(itr, knowledge, label="Knowledge")

def graphProduction(t, plt):
    "Production + DirectBuy"
    food = get_data(t, 'Food Production')
    food2 = get_data(t, 'Food DirectBuy')
    fooda = food + food2
    salt = get_data(t, 'Salt Production')
    salt2 = get_data(t, 'Salt DirectBuy')
    salta = salt + salt2
    fiber = get_data(t, 'Fiber Production')
    fiber2 = get_data(t, 'Fiber DirectBuy')
    fibera = fiber + fiber2
    fuel = get_data(t, 'Fuel Production')
    fuel2 = get_data(t, 'Fuel DirectBuy')
    fuela = fuel + fuel2
    raw = get_data(t, 'Raw Material Production')
    delicacies = get_data(t, 'Delicacies Production')
    exotic = get_data(t, 'Exotics Production')
    consumer = get_data(t, 'Consumer Product Production')
    military = get_data(t, 'Military Product Production')
    naval = get_data(t, 'Naval Product Production')
    industrial = get_data(t, 'Industrial Product Production')
    luxury = get_data(t, 'Luxury Product Production')
    knowledge = get_data(t, 'Knowledge Production')
    itr = range(1, len(food) + 1)

    plt.plot(itr, fooda, label="Food")
    plt.plot(itr, salta, label="Salt")
    plt.plot(itr, fibera, label="Fiber")
    plt.plot(itr, fuela, label="Fuel")
    plt.plot(itr, raw, label="Raw")
    plt.plot(itr, delicacies, label="Delicacies")
    plt.plot(itr, exotic, label="Exotics")
    plt.plot(itr, consumer, label="Consumer")
    plt.plot(itr, military, label="Military")
    plt.plot(itr, naval, label="Naval")
    plt.plot(itr, industrial, label="Industrial")
    plt.plot(itr, luxury, label="Luxury")
    plt.plot(itr, knowledge, label="Knowledge")

def graphBG_Income(t, plt):
        "Burgher Income"
        Total = get_data(t, 'Burgher Income Total')
        Innate = get_data(t, 'Burgher Income Innate')
        Tax = get_data(t, 'Burgher Income Tax')
        Property = get_data(t, 'Burgher Income Property')
        Prod = get_data(t, 'Burgher Income Prod')
        Wages = get_data(t, 'Burgher Income Wages')
        TaxFarm = get_data(t, 'Burgher Income Farm')
        Corruption = get_data(t, 'Burgher Income Corruption')
        itr = range(1, len(Total) + 1)

        plt.plot(itr, Total, label="Total")
        plt.plot(itr, Innate, label="Innate")
        plt.plot(itr, Tax, label="Tax")
        plt.plot(itr, Property, label="Property")
        plt.plot(itr, Prod, label="Prod")
        plt.plot(itr, Wages, label="Wages")
        plt.plot(itr, TaxFarm, label="Farm")
        plt.plot(itr, Corruption, label="Corruption")

def graphBG_Spend(t, plt):
        "Burgher Spending"
        Total = get_data(t, 'Burgher Spend Total')
        Tax = get_data(t, 'Burgher Spend Tax')
        Property = get_data(t, 'Burgher Spend Property')
        Infra = get_data(t, 'Burgher Spend Infra')
        Prod = get_data(t, 'Burgher Spend Prod')
        Manpower = get_data(t, 'Burgher Spend Manpower')
        itr = range(1, len(Total) + 1)

        plt.plot(itr, Total, label="Total")
        plt.plot(itr, Tax, label="Tax")
        plt.plot(itr, Property, label="Property")
        plt.plot(itr, Infra, label="Infra")
        plt.plot(itr, Prod, label="Prod")
        plt.plot(itr, Manpower, label="Manpower")

def graphBU_Tax(t, plt):
        "Bureaucracy Taxation"
        Direct = get_data(t, 'BUTax Direct')
        Indirect = get_data(t, 'BUTax Indirect')
        Revenue = get_data(t, 'BUTax Revenue')
        #Total = get_data(t, 'BUTax Total')
        # Fees = get_data(t, 'BUTax Fees')
        # Rents = get_data(t, 'BUTax Rents')
        Obligations = get_data(t, 'BUTax Obligations')
        Poll = get_data(t, 'BUTax Poll')
        # Land = get_data(t, 'BUTax Land')
        # PropertyBU = get_data(t, 'BUTax PropertyBU')
        # Chattel = get_data(t, 'BUTax Chattel')
        # Inheritance = get_data(t, 'BUTax Inheritance')
        # TollBU = get_data(t, 'BUTax TollBU')
        # SaltBU = get_data(t, 'BUTax SaltBU')
        # SubstancesBU = get_data(t, 'BUTax SubstancesBU')
        # TimberBU = get_data(t, 'BUTax TimberBU')
        # AlcoholBU = get_data(t, 'BUTax AlcoholBU')
        # ForestBU = get_data(t, 'BUTax ForestBU')
        Corruption = get_data(t, 'BUTax Corruption')
        Farming = get_data(t, 'BUTax Farming')
        # Special = get_data(t, 'BUTax Special')
        # Commerce = get_data(t, 'BUTax Commerce')
        BUProperty = get_data(t, 'BUTax BUProperty')
        itr = range(1, len(Poll) + 1)

        plt.plot(itr, Direct, label="Direct")
        plt.plot(itr, Indirect, label="Indirect")
        plt.plot(itr, Revenue, label="Revenue")
        #plt.plot(itr, Total, label="Total")
        plt.plot(itr, Obligations, label="Elite Obligations")
        plt.plot(itr, BUProperty, label="Property Income")
        plt.plot(itr, Farming, label="Rev Farming", linestyle='--')
        plt.plot(itr, Corruption, label="Corruption", linestyle='--')

def graphBU_Tax_All(t, plt):
        "Bureacracy Taxation (All)"
        #Direct = get_data(t, 'BUTax Direct')
        #Indirect = get_data(t, 'BUTax Indirect')
        #Revenue = get_data(t, 'BUTax Revenue')
        #Total = get_data(t, 'BUTax Total')
        Fees = get_data(t, 'BUTax Fees')
        Rents = get_data(t, 'BUTax Rents')
        Obligations = get_data(t, 'BUTax Obligations')
        Poll = get_data(t, 'BUTax Poll')
        Land = get_data(t, 'BUTax Land')
        PropertyBU = get_data(t, 'BUTax PropertyBU')
        Chattel = get_data(t, 'BUTax Chattel')
        Inheritance = get_data(t, 'BUTax Inheritance')
        TollBU = get_data(t, 'BUTax TollBU')
        SaltBU = get_data(t, 'BUTax SaltBU')
        SubstancesBU = get_data(t, 'BUTax SubstancesBU')
        TimberBU = get_data(t, 'BUTax TimberBU')
        AlcoholBU = get_data(t, 'BUTax AlcoholBU')
        ForestBU = get_data(t, 'BUTax ForestBU')
        #Corruption = get_data(t, 'BUTax Corruption')
        #Farming = get_data(t, 'BUTax Farming')
        Special = get_data(t, 'BUTax Special')
        Commerce = get_data(t, 'BUTax Commerce')
        # BUProperty = get_data(t, 'BUTax BUProperty')
        itr = range(1, len(Poll) + 1)

        #plt.plot(itr, Direct, label="Direct", linestyle='--')
        #plt.plot(itr, Indirect, label="Indirect", linestyle='--')
        #plt.plot(itr, Revenue, label="Revenue", linestyle='--')
        #plt.plot(itr, Farming, label="Rev Farming", linestyle='--')
        #plt.plot(itr, Corruption, label="Corruption", linestyle='--')
        #plt.plot(itr, Total, label="Total")
        plt.plot(itr, Obligations, label="Elite Obligations", linestyle='--')
        #plt.plot(itr, BUProperty, label="Property Income", linestyle='--')
        plt.plot(itr, Fees, label="Generic Fees", linestyle='--')
        plt.plot(itr, Rents, label="Feudal Rents", linestyle='--')
        plt.plot(itr, ForestBU, label="Forest Rents", linestyle='--')
        plt.plot(itr, Poll, label="Poll Tax", linestyle='--')
        plt.plot(itr, Land, label="Land Tax", linestyle='--')
        plt.plot(itr, PropertyBU, label="Property Tax", linestyle='--')
        plt.plot(itr, Chattel, label="Chattel Tax")
        plt.plot(itr, Inheritance, label="Inheritance Tax")
        plt.plot(itr, TollBU, label="Tolls")
        plt.plot(itr, SaltBU, label="Salt Excise")
        plt.plot(itr, SubstancesBU, label="Substances Excise")
        plt.plot(itr, TimberBU, label="Timber Excise")
        plt.plot(itr, AlcoholBU, label="Alcohol Excise")
        plt.plot(itr, Special, label="Special Taxes")
        plt.plot(itr, Commerce, label="Commerce Fees")

def graphClass_Balance(t, plt):
        "Class Balance"
        PeasantI = get_data(t, 'Peasant Income Total')
        PeasantS = get_data(t, 'Peasant Spend Total')
        NomadI = get_data(t, 'Nomad Income Total')
        NomadS = get_data(t, 'Nomad Spend Total')
        ResidentI = get_data(t, 'Resident Income Total')
        ResidentS = get_data(t, 'Resident Spend Total')
        NobleI = get_data(t, 'Noble Income Total')
        NobleS = get_data(t, 'Noble Spend Total')
        BurgherI = get_data(t, 'Burgher Income Total')
        BurgherS = get_data(t, 'Burgher Spend Total')
        ClergyI = get_data(t, 'Clergy Income Total')
        ClergyS = get_data(t, 'Clergy Spend Total')
        itr = range(1, len(PeasantI) + 1)
        PeasantI = [PeasantI[i]-PeasantS[i] for i in range(len(PeasantI))]
        NomadI = [NomadI[i]-NomadS[i] for i in range(len(PeasantI))]
        ResidentI = [ResidentI[i]-ResidentS[i] for i in range(len(PeasantI))]
        NobleI = [NobleI[i]-NobleS[i] for i in range(len(PeasantI))]
        BurgherI = [BurgherI[i]-BurgherS[i] for i in range(len(PeasantI))]
        ClergyI = [ClergyI[i]-ClergyS[i] for i in range(len(PeasantI))]

        plt.plot(itr, PeasantI, label="Peasants")
        plt.plot(itr, NomadI, label="Nomads")
        plt.plot(itr, ResidentI, label="Residents")
        plt.plot(itr, NobleI, label="Nobles")
        plt.plot(itr, BurgherI, label="Burghers")
        plt.plot(itr, ClergyI, label="Clergy")

def graphClass_Balance_Prop(t, plt):
        "Class Balance (Property)"
        PeasantI = get_data(t, 'Peasant Income Property')
        PeasantS = get_data(t, 'Peasant Spend Property')
        NomadI = get_data(t, 'Nomad Income Property')
        NomadS = get_data(t, 'Nomad Spend Property')
        ResidentI = get_data(t, 'Resident Income Property')
        ResidentS = get_data(t, 'Resident Spend Property')
        NobleI = get_data(t, 'Noble Income Property')
        NobleS = get_data(t, 'Noble Spend Property')
        BurgherI = get_data(t, 'Burgher Income Property')
        BurgherS = get_data(t, 'Burgher Spend Property')
        ClergyI = get_data(t, 'Clergy Income Property')
        ClergyS = get_data(t, 'Clergy Spend Property')
        itr = range(1, len(PeasantI) + 1)
        PeasantI = [PeasantI[i]-PeasantS[i] for i in range(len(PeasantI))]
        NomadI = [NomadI[i]-NomadS[i] for i in range(len(PeasantI))]
        ResidentI = [ResidentI[i]-ResidentS[i] for i in range(len(PeasantI))]
        NobleI = [NobleI[i]-NobleS[i] for i in range(len(PeasantI))]
        BurgherI = [BurgherI[i]-BurgherS[i] for i in range(len(PeasantI))]
        ClergyI = [ClergyI[i]-ClergyS[i] for i in range(len(PeasantI))]

        plt.plot(itr, PeasantI, label="Peasants")
        plt.plot(itr, NomadI, label="Nomads")
        plt.plot(itr, ResidentI, label="Residents")
        plt.plot(itr, NobleI, label="Nobles")
        plt.plot(itr, BurgherI, label="Burghers")
        plt.plot(itr, ClergyI, label="Clergy")

def graphClass_Income(t, plt):
        "Class Income"
        sfwealth = get_data(t, 'Peasant Income Total')
        nmwealth = get_data(t, 'Nomad Income Total')
        rewealth = get_data(t, 'Resident Income Total')
        nowealth = get_data(t, 'Noble Income Total')
        bgwealth = get_data(t, 'Burgher Income Total')
        clwealth = get_data(t, 'Clergy Income Total')
        itr = range(1, len(sfwealth) + 1)

        #plt.plot(itr, wage, label="Total")
        plt.plot(itr, sfwealth, label="Peasant")
        plt.plot(itr, nmwealth, label="Nomad")
        plt.plot(itr, rewealth, label="Resident")
        plt.plot(itr, nowealth, label="Noble")
        plt.plot(itr, bgwealth, label="Burgher")
        plt.plot(itr, clwealth, label="Clergy")

def graphClass_Spend(t, plt):
        "Class Spending"
        sfwealth = get_data(t, 'Peasant Spend Total')
        nmwealth = get_data(t, 'Nomad Spend Total')
        rewealth = get_data(t, 'Resident Spend Total')
        nowealth = get_data(t, 'Noble Spend Total')
        bgwealth = get_data(t, 'Burgher Spend Total')
        clwealth = get_data(t, 'Clergy Spend Total')
        itr = range(1, len(sfwealth) + 1)

        #plt.plot(itr, wage, label="Total")
        plt.plot(itr, sfwealth, label="Peasant")
        plt.plot(itr, nmwealth, label="Nomad")
        plt.plot(itr, rewealth, label="Resident")
        plt.plot(itr, nowealth, label="Noble")
        plt.plot(itr, bgwealth, label="Burgher")
        plt.plot(itr, clwealth, label="Clergy")

def graphClass_Wealth(t, plt):
        "Class Wealth"
        sfwealth = get_data(t, 'Peasant Wealth')
        nmwealth = get_data(t, 'Nomad Wealth')
        rewealth = get_data(t, 'Resident Wealth')
        nowealth = get_data(t, 'Noble Wealth')
        bgwealth = get_data(t, 'Burgher Wealth')
        clwealth = get_data(t, 'Clergy Wealth')
        itr = range(1, len(sfwealth) + 1)

        #plt.plot(itr, wage, label="Total")
        plt.plot(itr, sfwealth, label="Peasant")
        plt.plot(itr, nmwealth, label="Nomad")
        plt.plot(itr, rewealth, label="Resident")
        plt.plot(itr, nowealth, label="Noble")
        plt.plot(itr, bgwealth, label="Burgher")
        plt.plot(itr, clwealth, label="Clergy")

def graphCL_Income(t, plt):
        "Clergy Income"
        Total = get_data(t, 'Clergy Income Total')
        Innate = get_data(t, 'Clergy Income Innate')
        Tax = get_data(t, 'Clergy Income Tax')
        Property = get_data(t, 'Clergy Income Property')
        Prod = get_data(t, 'Clergy Income Prod')
        Wages = get_data(t, 'Clergy Income Wages')
        TaxFarm = get_data(t, 'Clergy Income Farm')
        Corruption = get_data(t, 'Clergy Income Corruption')
        itr = range(1, len(Total) + 1)

        plt.plot(itr, Total, label="Total")
        plt.plot(itr, Innate, label="Innate")
        plt.plot(itr, Tax, label="Tax")
        plt.plot(itr, Property, label="Property")
        plt.plot(itr, Prod, label="Prod")
        plt.plot(itr, Wages, label="Wages")
        plt.plot(itr, TaxFarm, label="Farm")
        plt.plot(itr, Corruption, label="Corruption")

def graphCL_Spend(t, plt):
        "Clergy Spending"
        Total = get_data(t, 'Clergy Spend Total')
        Tax = get_data(t, 'Clergy Spend Tax')
        Property = get_data(t, 'Clergy Spend Property')
        # Infra = get_data(t, 'Clergy Spend Infra')
        Prod = get_data(t, 'Clergy Spend Prod')
        #Manpower = get_data(t, 'Clergy Spend Manpower')
        itr = range(1, len(Total) + 1)

        plt.plot(itr, Total, label="Total")
        plt.plot(itr, Tax, label="Tax")
        plt.plot(itr, Property, label="Property")
        # plt.plot(itr, Infra, label="Infra")
        plt.plot(itr, Prod, label="Prod")
        # plt.plot(itr, Manpower, label="Manpower")

def graphCommerce_GV(t, plt):
        "Commercial Size"
        Genoa = get_data(t, 'Genoa commercial size')
        Venice = get_data(t, 'Venice commercial size')
        Paris = get_data(t, 'Paris commercial size')
        London = get_data(t, 'London commercial size')
        Lübeck = get_data(t, 'Lübeck commercial size')
        Konstantinople = get_data(t, 'Konstantinople commercial size')
        AlQahira = get_data(t, 'Al Qahira commercial size')
        itr = range(1, len(Genoa) + 1)

        plt.plot(itr, Genoa, label="Genoa")
        plt.plot(itr, Venice, label="Venice")
        plt.plot(itr, Paris, label="Paris")
        plt.plot(itr, London, label="London")
        plt.plot(itr, Lübeck, label="Lübeck")
        plt.plot(itr, Konstantinople, label="Konstantinople")
        plt.plot(itr, AlQahira, label="AlQahira")

def graphFiber_Diff(t, plt):
        "Fiber (Supply - Demand)"
        food = get_data(t, 'Europe Fiber R Supply')
        salt = get_data(t, 'ME Fiber R Supply')
        fiber = get_data(t, 'Africa Fiber R Supply')
        fuel = get_data(t, 'India Fiber R Supply')
        raw = get_data(t, 'SEA Fiber R Supply')
        delicacies = get_data(t, 'Asia Fiber R Supply')
        exotic = get_data(t, 'CA Fiber R Supply')
        consumer = get_data(t, 'SA Fiber R Supply')
        military = get_data(t, 'NA Fiber R Supply')
        food2 = get_data(t, 'Europe Fiber R Demand')
        salt2 = get_data(t, 'ME Fiber R Demand')
        fiber2 = get_data(t, 'Africa Fiber R Demand')
        fuel2 = get_data(t, 'India Fiber R Demand')
        raw2 = get_data(t, 'SEA Fiber R Demand')
        delicacies2 = get_data(t, 'Asia Fiber R Demand')
        exotic2 = get_data(t, 'CA Fiber R Demand')
        consumer2 = get_data(t, 'SA Fiber R Demand')
        #military2 = get_data(t, 'NA Fiber R Demand')
        itr = range(1, len(food) + 1)
        food = [food[i]-food2[i] for i in range(len(food))]
        salt = [salt[i]-salt2[i] for i in range(len(salt))]
        fiber = [fiber[i]-fiber2[i] for i in range(len(fiber))]
        fuel = [fuel[i]-fuel2[i] for i in range(len(fuel))]
        raw = [raw[i]-raw2[i] for i in range(len(raw))]
        delicacies = [delicacies[i]-delicacies2[i] for i in range(len(delicacies))]
        exotic = [exotic[i]-exotic2[i] for i in range(len(exotic))]
        consumer = [consumer[i]-consumer2[i] for i in range(len(consumer))]
        # military = [military[i]-military2[i] for i in range(len(military))]

        plt.plot(itr, food, label="Europe")
        plt.plot(itr, salt, label="Middle East")
        plt.plot(itr, fiber, label="Africa")
        plt.plot(itr, fuel, label="India")
        plt.plot(itr, raw, label="Southeast Asia")
        plt.plot(itr, delicacies, label="Asia + Japan")
        plt.plot(itr, exotic, label="Central Asia")
        plt.plot(itr, consumer, label="South America")
        #plt.plot(itr, military, label="North America")

def graphFiber(t, plt):
        "Fiber Data"
        Fiberp = np.array(get_data(t, 'Fiber Production'))
        Fiberd = np.array(get_data(t, 'Fiber Demand'))
        Fibere = np.array(get_data(t, 'Fiber DirectBuy'))
        Fiberf = Fiberd + Fibere
        Fiberj = Fiberp + Fibere
        itr = range(1, len(Fiberp) + 1)

        plt.plot(itr, Fiberp, label="Production")
        plt.plot(itr, Fiberd, label="Market Demand")
        plt.plot(itr, Fibere, label="Direct Buy")
        plt.plot(itr, Fiberf, label="Total Demand")
        plt.plot(itr, Fiberj, label="Total Production")

def graphFood_Africa(t, plt):
        "Food (Africa)"
        foodp = np.array(get_data(t, 'Africa Food R Supply'))
        foodd = np.array(get_data(t, 'Africa Food R Demand'))
        foode = np.array(get_data(t, 'Africa Food R Direct'))
        foodf = foodd + foode
        foodj = foodp + foode
        itr = range(1, len(foodp) + 1)

        plt.plot(itr, foodp, label="Production")
        plt.plot(itr, foodd, label="Market Demand")
        plt.plot(itr, foode, label="Direct Buy")
        plt.plot(itr, foodf, label="Total Demand")
        plt.plot(itr, foodj, label="Total Production")

def graphFood_Asia(t, plt):
        "Food (Asia)"
        foodp = np.array(get_data(t, 'Asia Food R Supply'))
        foodd = np.array(get_data(t, 'Asia Food R Demand'))
        foode = np.array(get_data(t, 'Asia Food R Direct'))
        foodf = foodd + foode
        foodj = foodp + foode
        itr = range(1, len(foodp) + 1)

        plt.plot(itr, foodp, label="Production")
        plt.plot(itr, foodd, label="Market Demand")
        plt.plot(itr, foode, label="Direct Buy")
        plt.plot(itr, foodf, label="Total Demand")
        plt.plot(itr, foodj, label="Total Production")

def graphFood_Central_Asia(t, plt):
        "Food (Central Asia)"
        foodp = np.array(get_data(t, 'CA Food R Supply'))
        foodd = np.array(get_data(t, 'CA Food R Demand'))
        foode = np.array(get_data(t, 'CA Food R Direct'))
        foodf = foodd + foode
        foodj = foodp + foode
        itr = range(1, len(foodp) + 1)

        plt.plot(itr, foodp, label="Production")
        plt.plot(itr, foodd, label="Market Demand")
        plt.plot(itr, foode, label="Direct Buy")
        plt.plot(itr, foodf, label="Total Demand")
        plt.plot(itr, foodj, label="Total Production")

def graphFood_Diff(t, plt):
        "Food (Supply - Demand)"
        food = get_data(t, 'Europe Food R Supply')
        salt = get_data(t, 'ME Food R Supply')
        fiber = get_data(t, 'Africa Food R Supply')
        fuel = get_data(t, 'India Food R Supply')
        raw = get_data(t, 'SEA Food R Supply')
        delicacies = get_data(t, 'Asia Food R Supply')
        exotic = get_data(t, 'CA Food R Supply')
        consumer = get_data(t, 'SA Food R Supply')
        military = get_data(t, 'NA Food R Supply')
        food2 = get_data(t, 'Europe Food R Demand')
        salt2 = get_data(t, 'ME Food R Demand')
        fiber2 = get_data(t, 'Africa Food R Demand')
        fuel2 = get_data(t, 'India Food R Demand')
        raw2 = get_data(t, 'SEA Food R Demand')
        delicacies2 = get_data(t, 'Asia Food R Demand')
        exotic2 = get_data(t, 'CA Food R Demand')
        consumer2 = get_data(t, 'SA Food R Demand')
        military2 = get_data(t, 'NA Food R Demand')
        itr = range(1, len(food) + 1)
        food = [food[i]-food2[i] for i in range(len(food))]
        salt = [salt[i]-salt2[i] for i in range(len(salt))]
        fiber = [fiber[i]-fiber2[i] for i in range(len(fiber))]
        fuel = [fuel[i]-fuel2[i] for i in range(len(fuel))]
        raw = [raw[i]-raw2[i] for i in range(len(raw))]
        delicacies = [delicacies[i]-delicacies2[i] for i in range(len(delicacies))]
        exotic = [exotic[i]-exotic2[i] for i in range(len(exotic))]
        consumer = [consumer[i]-consumer2[i] for i in range(len(consumer))]
        military = [military[i]-military2[i] for i in range(len(military))]

        plt.plot(itr, food, label="Europe")
        plt.plot(itr, salt, label="Middle East")
        plt.plot(itr, fiber, label="Africa")
        plt.plot(itr, fuel, label="India")
        plt.plot(itr, raw, label="Southeast Asia")
        plt.plot(itr, delicacies, label="Asia + Japan")
        plt.plot(itr, exotic, label="Central Asia")
        plt.plot(itr, consumer, label="South America")
        plt.plot(itr, military, label="North America")

def graphFood_Europe(t, plt):
        "Food (Europe)"
        foodp = np.array(get_data(t, 'Europe Food R Supply'))
        foodd = np.array(get_data(t, 'Europe Food R Demand'))
        foode = np.array(get_data(t, 'Europe Food R Direct'))
        foodf = foodd + foode
        foodj = foodp + foode
        itr = range(1, len(foodp) + 1)

        plt.plot(itr, foodp, label="Production")
        plt.plot(itr, foodd, label="Market Demand")
        plt.plot(itr, foode, label="Direct Buy")
        plt.plot(itr, foodf, label="Total Demand")
        plt.plot(itr, foodj, label="Total Production")

def graphFood_India(t, plt):
        "Food (India)"
        foodp = np.array(get_data(t, 'India Food R Supply'))
        foodd = np.array(get_data(t, 'India Food R Demand'))
        foode = np.array(get_data(t, 'India Food R Direct'))
        foodf = foodd + foode
        foodj = foodp + foode
        itr = range(1, len(foodp) + 1)

        plt.plot(itr, foodp, label="Production")
        plt.plot(itr, foodd, label="Market Demand")
        plt.plot(itr, foode, label="Direct Buy")
        plt.plot(itr, foodf, label="Total Demand")
        plt.plot(itr, foodj, label="Total Production")

def graphFood_MENA(t, plt):
        "Food (Middle East & North Africa)"
        foodp = np.array(get_data(t, 'ME Food R Production'))
        foodd = np.array(get_data(t, 'ME Food R Demand'))
        foode = np.array(get_data(t, 'ME Food R Direct'))
        foodf = foodd + foode
        foodj = foodp + foode
        itr = range(1, len(foodp) + 1)

        plt.plot(itr, foodp, label="Production")
        plt.plot(itr, foodd, label="Market Demand")
        plt.plot(itr, foode, label="Direct Buy")
        plt.plot(itr, foodf, label="Total Demand")
        plt.plot(itr, foodj, label="Total Production")

def graphFood_NA(t, plt):
        "Food (North America)"
        foodp = np.array(get_data(t, 'NA Food R Production'))
        foodd = np.array(get_data(t, 'NA Food R Demand'))
        foode = np.array(get_data(t, 'NA Food R Direct'))
        foodf = foodd + foode
        foodj = foodp + foode
        itr = range(1, len(foodp) + 1)

        plt.plot(itr, foodp, label="Production")
        plt.plot(itr, foodd, label="Market Demand")
        plt.plot(itr, foode, label="Direct Buy")
        plt.plot(itr, foodf, label="Total Demand")
        plt.plot(itr, foodj, label="Total Production")

def graphFood_SEA(t, plt):
        "Food (South-East Asia)"
        foodp = np.array(get_data(t, 'SEA Food R Production'))
        foodd = np.array(get_data(t, 'SEA Food R Demand'))
        foode = np.array(get_data(t, 'SEA Food R Direct'))
        foodf = foodd + foode
        foodj = foodp + foode
        itr = range(1, len(foodp) + 1)

        plt.plot(itr, foodp, label="Production")
        plt.plot(itr, foodd, label="Market Demand")
        plt.plot(itr, foode, label="Direct Buy")
        plt.plot(itr, foodf, label="Total Demand")
        plt.plot(itr, foodj, label="Total Production")

def graphFood_SA(t, plt):
        "Food (South America)"
        foodp = np.array(get_data(t, 'SA Food R Production'))
        foodd = np.array(get_data(t, 'SA Food R Demand'))
        foode = np.array(get_data(t, 'SA Food R Direct'))
        foodf = foodd + foode
        foodj = foodp + foode
        itr = range(1, len(foodp) + 1)

        plt.plot(itr, foodp, label="Production")
        plt.plot(itr, foodd, label="Market Demand")
        plt.plot(itr, foode, label="Direct Buy")
        plt.plot(itr, foodf, label="Total Demand")
        plt.plot(itr, foodj, label="Total Production")

def graphFood(t, plt):
        "Food Data"
        foodp = np.array(get_data(t, 'Food Production'))
        foodd = np.array(get_data(t, 'Food Demand'))
        foode = np.array(get_data(t, 'Food DirectBuy'))
        foodf = foodd + foode
        foodj = foodp + foode
        itr = range(1, len(foodp) + 1)

        plt.plot(itr, foodp, label="Production")
        plt.plot(itr, foodd, label="Market Demand")
        plt.plot(itr, foode, label="Direct Buy")
        plt.plot(itr, foodf, label="Total Demand")
        plt.plot(itr, foodj, label="Total Production")

def graphFuel(t, plt):
        "Fuel Data"
        Fuelp = np.array(get_data(t, 'Fuel Production'))
        Fueld = np.array(get_data(t, 'Fuel Demand'))
        Fuele = np.array(get_data(t, 'Fuel DirectBuy'))
        Fuelf = Fueld + Fuele
        Fuelj = Fuelp + Fuele
        itr = range(1, len(Fuelp) + 1)

        plt.plot(itr, Fuelp, label="Production")
        plt.plot(itr, Fueld, label="Market Demand")
        plt.plot(itr, Fuele, label="Direct Buy")
        plt.plot(itr, Fuelf, label="Total Demand")
        plt.plot(itr, Fuelj, label="Total Production")

def graphInfra(t, plt):
        "Infrastructure Wealth"
        wealth = get_data(t, 'Infra Wealth')
        itr = range(1, len(wealth) + 1)

        #plt.plot(itr, wage, label="Total")
        plt.plot(itr, wealth, label="Wealth")

def graphInfra_Class(t, plt):
        "Infrastructure Class Spending"
        sfwealth = get_data(t, 'Peasant Spend Infra')
        nmwealth = get_data(t, 'Nomad Spend Infra')
        rewealth = get_data(t, 'Resident Spend Infra')
        nowealth = get_data(t, 'Noble Spend Infra')
        bgwealth = get_data(t, 'Burgher Spend Infra')
        clwealth = get_data(t, 'Clergy Spend Infra')
        itr = range(1, len(sfwealth) + 1)

        #plt.plot(itr, wage, label="Total")
        plt.plot(itr, sfwealth, label="Peasant")
        plt.plot(itr, nmwealth, label="Nomad")
        plt.plot(itr, rewealth, label="Resident")
        plt.plot(itr, nowealth, label="Noble")
        plt.plot(itr, bgwealth, label="Burgher")
        plt.plot(itr, clwealth, label="Clergy")

def graphLabor_Balance(t, plt):
        "Labor Funding - Cost"
        SF = get_data(t, 'Labor Funded R')
        NM = get_data(t, 'Labor Funded NM')
        RE = get_data(t, 'Labor Funded UL')
        NO = get_data(t, 'Labor Funded NO')
        BG = get_data(t, 'Labor Funded BG')
        CL = get_data(t, 'Labor Funded CL')
        BU = get_data(t, 'Labor Funded LT')
        SF2 = get_data(t, 'Labor Cost R')
        NM2 = get_data(t, 'Labor Cost NM')
        RE2 = get_data(t, 'Labor Cost UL')
        NO2 = get_data(t, 'Labor Cost NO')
        BG2 = get_data(t, 'Labor Cost BG')
        CL2 = get_data(t, 'Labor Cost CL')
        BU2 = get_data(t, 'Labor Cost LT')
        itr = range(1, len(SF) + 1)
        SF = [SF[i]-SF2[i] for i in range(len(SF))]
        NM = [NM[i]-NM2[i] for i in range(len(NM))]
        RE = [RE[i]-RE2[i] for i in range(len(RE))]
        NO = [NO[i]-NO2[i] for i in range(len(NO))]
        BG = [BG[i]-BG2[i] for i in range(len(BG))]
        CL = [CL[i]-CL2[i] for i in range(len(CL))]
        BU = [BU[i]-BU2[i] for i in range(len(BU))]

        plt.plot(itr, SF, label="Peasants")
        plt.plot(itr, NM, label="Nomads")
        plt.plot(itr, RE, label="Residents")
        plt.plot(itr, NO, label="Nobles")
        plt.plot(itr, BG, label="Burghers")
        plt.plot(itr, CL, label="Clergy")
        plt.plot(itr, BU, label="State")

def graphLabor_Cost(t, plt):
        "Labor Cost"
        SF = get_data(t, 'Labor Cost R')
        NM = get_data(t, 'Labor Cost NM')
        RE = get_data(t, 'Labor Cost UL')
        NO = get_data(t, 'Labor Cost NO')
        BG = get_data(t, 'Labor Cost BG')
        CL = get_data(t, 'Labor Cost CL')
        BU = get_data(t, 'Labor Cost LT')
        itr = range(1, len(SF) + 1)

        plt.plot(itr, SF, label="Rural")
        plt.plot(itr, NM, label="Nomads")
        plt.plot(itr, RE, label="Urban")
        plt.plot(itr, NO, label="Nobles")
        plt.plot(itr, BG, label="Burghers")
        plt.plot(itr, CL, label="Clergy")
        plt.plot(itr, BU, label="Literati")

def graphLabor_Funding(t, plt):
        "Labor Funding"
        SF = get_data(t, 'Labor Funded R')
        NM = get_data(t, 'Labor Funded NM')
        RE = get_data(t, 'Labor Funded UL')
        NO = get_data(t, 'Labor Funded NO')
        BG = get_data(t, 'Labor Funded BG')
        CL = get_data(t, 'Labor Funded CL')
        BU = get_data(t, 'Labor Funded LT')
        itr = range(1, len(SF) + 1)

        plt.plot(itr, SF, label="Rural")
        plt.plot(itr, NM, label="Nomads")
        plt.plot(itr, RE, label="Urban")
        plt.plot(itr, NO, label="Nobles")
        plt.plot(itr, BG, label="Burghers")
        plt.plot(itr, CL, label="Clergy")
        plt.plot(itr, BU, label="Literati")

def graphLabor_Money(t, plt):
        "Labor Funds Available"
        SF = get_data(t, 'Labor SF Fund')
        NM = get_data(t, 'Labor NM Fund')
        RE = get_data(t, 'Labor RE Fund')
        NO = get_data(t, 'Labor NO Fund')
        BG = get_data(t, 'Labor BG Fund')
        CL = get_data(t, 'Labor CL Fund')
        BU = get_data(t, 'Labor BU Fund')
        itr = range(1, len(SF) + 1)

        plt.plot(itr, SF, label="Peasants")
        plt.plot(itr, NM, label="Nomads")
        plt.plot(itr, RE, label="Residents")
        plt.plot(itr, NO, label="Nobles")
        plt.plot(itr, BG, label="Burghers")
        plt.plot(itr, CL, label="Clergy")
        plt.plot(itr, BU, label="State")

def graphLabor_Wages(t, plt):
        "Labor Wages"
        food1 = get_data(t, 'Rural Wage')
        food2 = get_data(t, 'Nomad Wage')
        food3 = get_data(t, 'Urban Wage')
        food4 = get_data(t, 'Burgher Wage')
        food5 = get_data(t, 'Literati Wage')
        food6 = get_data(t, 'Clergy Wage')
        itr = range(1, len(food1) + 1)

        plt.plot(itr, food1, label="Rural")
        plt.plot(itr, food2, label="Nomad")
        plt.plot(itr, food3, label="Urban")
        plt.plot(itr, food4, label="Burgher")
        plt.plot(itr, food5, label="Literati")
        plt.plot(itr, food6, label="Clergy")

def graphNM_Income(t, plt):
        "Nomads Income"
        Total = get_data(t, 'Nomad Income Total')
        Innate = get_data(t, 'Nomad Income Innate')
        Tax = get_data(t, 'Nomad Income Tax')
        Property = get_data(t, 'Nomad Income Property')
        Prod = get_data(t, 'Nomad Income Prod')
        itr = range(1, len(Total) + 1)

        plt.plot(itr, Total, label="Total")
        plt.plot(itr, Innate, label="Innate")
        plt.plot(itr, Tax, label="Tax")
        plt.plot(itr, Property, label="Property")
        plt.plot(itr, Prod, label="Prod")

def graphNO_Income(t, plt):
        "Nobles Income"
        Total = get_data(t, 'Noble Income Total')
        Innate = get_data(t, 'Noble Income Innate')
        Tax = get_data(t, 'Noble Income Tax')
        Property = get_data(t, 'Noble Income Property')
        Prod = get_data(t, 'Noble Income Prod')
        Wages = get_data(t, 'Noble Income Wages')
        TaxFarm = get_data(t, 'Noble Income Farm')
        Corruption = get_data(t, 'Noble Income Corruption')
        itr = range(1, len(Total) + 1)

        plt.plot(itr, Total, label="Total")
        plt.plot(itr, Innate, label="Innate")
        plt.plot(itr, Tax, label="Tax")
        plt.plot(itr, Property, label="Property")
        plt.plot(itr, Prod, label="Prod")
        plt.plot(itr, Wages, label="Wages")
        plt.plot(itr, TaxFarm, label="Farm")
        plt.plot(itr, Corruption, label="Corruption")

def graphNon_High_Demand(t, plt):
        "<please explain>"
        food = get_data(t, 'Food Demand')
        salt = get_data(t, 'Salt Demand')
        fiber = get_data(t, 'Fiber Demand')
        fuel = get_data(t, 'Fuel Demand')
        raw = get_data(t, 'Raw Material Demand')
        delicacies = get_data(t, 'Delicacies Demand')
        exotic = get_data(t, 'Exotics Demand')
        consumer = get_data(t, 'Consumer Product Demand')
        military = get_data(t, 'Military Product Demand')
        naval = get_data(t, 'Naval Product Demand')
        industrial = get_data(t, 'Industrial Product Demand')
        luxury = get_data(t, 'Luxury Product Demand')
        knowledge = get_data(t, 'Knowledge Demand')
        itr = range(1, len(food) + 1)

        #plt.plot(itr, food, label="Food")
        plt.plot(itr, salt, label="Salt")
        plt.plot(itr, fiber, label="Fiber")
        plt.plot(itr, fuel, label="Fuel")
        plt.plot(itr, raw, label="Raw")
        plt.plot(itr, delicacies, label="Delicacies")
        plt.plot(itr, exotic, label="Exotic")
        plt.plot(itr, consumer, label="Consumer")
        plt.plot(itr, military, label="Military")
        plt.plot(itr, naval, label="Naval")
        plt.plot(itr, industrial, label="Industrial")
        plt.plot(itr, luxury, label="Luxury")
        plt.plot(itr, knowledge, label="Knowledge")

def graphNon_High_Other(t, plt):
        "<please explain>"
        pwealth = get_data(t, 'Peasant Wealth')
        nwealth = get_data(t, 'Nomad Wealth')
        rwealth = get_data(t, 'Resident Wealth')
        nowealth = get_data(t, 'Noble Wealth')
        bwealth = get_data(t, 'Burgher Wealth')
        cwealth = get_data(t, 'Clergy Wealth')
        #wealth = get_data(t, 'Wealth')
        itr = range(1, len(pwealth) + 1)

        #plt.plot(itr, wage, label="Total")
        plt.plot(itr, pwealth, label="Peasants")
        plt.plot(itr, nwealth, label="Nomads")
        plt.plot(itr, rwealth, label="Residents")
        plt.plot(itr, nowealth, label="Nobles")
        plt.plot(itr, bwealth, label="Burghers")
        plt.plot(itr, cwealth, label="Clergy")
        #plt.plot(itr, wealth, label="Wealth")

def graphNon_High_Price(t, plt):
        "<please explain>"
        food = get_data(t, 'Global Food Price')
        salt = get_data(t, 'Global Salt Price')
        fiber = get_data(t, 'Global Fiber Price')
        fuel = get_data(t, 'Global Fuel Price')
        raw = get_data(t, 'Global Raw Material Price')
        delicacies = get_data(t, 'Global Delicacies Price')
        exotic = get_data(t, 'Global Exotics Price')
        consumer = get_data(t, 'Global Consumer Product Price')
        military = get_data(t, 'Global Military Product Price')
        naval = get_data(t, 'Global Naval Product Price')
        industrial = get_data(t, 'Global Industrial Product Price')
        luxury = get_data(t, 'Global Luxury Product Price')
        knowledge = get_data(t, 'Global Knowledge Price')
        itr = range(1, len(food) + 1)

        plt.plot(itr, food, label="Food")
        plt.plot(itr, salt, label="Salt")
        plt.plot(itr, fiber, label="Fiber")
        plt.plot(itr, fuel, label="Fuel")
        plt.plot(itr, raw, label="Raw")
        #plt.plot(itr, delicacies, label="Delicacies")
        #plt.plot(itr, exotic, label="Exotics")
        plt.plot(itr, consumer, label="Consumer")
        plt.plot(itr, military, label="Military")
        plt.plot(itr, naval, label="Naval")
        plt.plot(itr, industrial, label="Industrial")
        #plt.plot(itr, luxury, label="Luxury")
        #plt.plot(itr, knowledge, label="Knowledge")

def graphNon_High_Prod(t, plt):
        "<please explain>"
        food = get_data(t, 'Food Production')
        food2 = get_data(t, 'Food DirectBuy')
        fooda = food + food2
        salt = get_data(t, 'Salt Production')
        salt2 = get_data(t, 'Salt DirectBuy')
        salta = salt + salt2
        fiber = get_data(t, 'Fiber Production')
        fiber2 = get_data(t, 'Fiber DirectBuy')
        fibera = fiber + fiber2
        fuel = get_data(t, 'Fuel Production')
        fuel2 = get_data(t, 'Fuel DirectBuy')
        fuela = fuel + fuel2
        raw = get_data(t, 'Raw Material Production')
        delicacies = get_data(t, 'Delicacies Production')
        exotic = get_data(t, 'Exotics Production')
        consumer = get_data(t, 'Consumer Product Production')
        military = get_data(t, 'Military Product Production')
        naval = get_data(t, 'Naval Product Production')
        industrial = get_data(t, 'Industrial Product Production')
        luxury = get_data(t, 'Luxury Product Production')
        knowledge = get_data(t, 'Knowledge Production')
        itr = range(1, len(food) + 1)

        #plt.plot(itr, fooda, label="Food")
        plt.plot(itr, salta, label="Salt")
        plt.plot(itr, fibera, label="Fiber")
        plt.plot(itr, fuela, label="Fuel")
        plt.plot(itr, raw, label="Raw")
        plt.plot(itr, delicacies, label="Delicacies")
        plt.plot(itr, exotic, label="Exotics")
        plt.plot(itr, consumer, label="Consumer")
        plt.plot(itr, military, label="Military")
        plt.plot(itr, naval, label="Naval")
        plt.plot(itr, industrial, label="Industrial")
        plt.plot(itr, luxury, label="Luxury")
        plt.plot(itr, knowledge, label="Knowledge")

def graphNO_Spend(t, plt):
        "Nobles Spending"
        Total = get_data(t, 'Noble Spend Total')
        Prod = get_data(t, 'Noble Spend Prod')
        Property = get_data(t, 'Noble Spend Property')
        Infra = get_data(t, 'Noble Spend Infra')
        Tax = get_data(t, 'Noble Spend Tax')
        Manpower = get_data(t, 'Noble Spend Manpower')
        itr = range(1, len(Total) + 1)

        plt.plot(itr, Total, label="Total")
        plt.plot(itr, Tax, label="Tax")
        plt.plot(itr, Property, label="Property")
        plt.plot(itr, Prod, label="Prod")
        plt.plot(itr, Manpower, label="Manpower")
        plt.plot(itr, Infra, label="Infra")

def graphFulfill_Comfort(t, plt):
        "Comfort Needs Fulfillment"
        #Class = get_data(t, 'Class Pop')
        SF = get_data(t, 'Fulfil SF Comfort')
        NM = get_data(t, 'Fulfil NM Comfort')
        RE = get_data(t, 'Fulfil RE Comfort')
        NO = get_data(t, 'Fulfil NO Comfort')
        BG = get_data(t, 'Fulfil BG Comfort')
        CL = get_data(t, 'Fulfil CL Comfort')
        itr = range(1, len(SF) + 1)

        #plt.plot(itr, Class, label="Total")
        plt.plot(itr, SF, label="Peasants")
        plt.plot(itr, NM, label="Nomads")
        plt.plot(itr, NO, label="Nobles")
        plt.plot(itr, CL, label="Clergy")
        plt.plot(itr, RE, label="Residents")
        plt.plot(itr, BG, label="Burghers")

def graphFulfill_Food(t, plt):
        "Food Needs Fulfillment"
        #Class = get_data(t, 'Class Pop Total')
        SF = get_data(t, 'Fulfil SF Food')
        NM = get_data(t, 'Fulfil NM Food')
        RE = get_data(t, 'Fulfil RE Food')
        NO = get_data(t, 'Fulfil NO Food')
        BG = get_data(t, 'Fulfil BG Food')
        CL = get_data(t, 'Fulfil CL Food')
        SFD = get_data(t, 'Fulfil SF Direct Food')
        NMD = get_data(t, 'Fulfil NM Direct Food')
        NOD = get_data(t, 'Fulfil NO Direct Food')
        CLD = get_data(t, 'Fulfil CL Direct Food')
        itr = range(1, len(SF) + 1)

        #plt.plot(itr, Class, label="Total")
        plt.plot(itr, SF, label="Peasants Total")
        plt.plot(itr, NM, label="Nomads Total")
        plt.plot(itr, NO, label="Nobles Total")
        plt.plot(itr, CL, label="Clergy Total")
        plt.plot(itr, RE, label="Residents")
        plt.plot(itr, BG, label="Burghers")
        plt.plot(itr, SFD, label="Peasants Direct")
        plt.plot(itr, NMD, label="Nomads Direct")
        plt.plot(itr, NOD, label="Nobles Direct")
        plt.plot(itr, CLD, label="Clergy Direct")

def graphFulfill_Life(t, plt):
        "Life Needs Fulfillment"
        #Class = get_data(t, 'Class Pop Total')
        SF = get_data(t, 'Fulfil SF Life')
        NM = get_data(t, 'Fulfil NM Life')
        RE = get_data(t, 'Fulfil RE Life')
        NO = get_data(t, 'Fulfil NO Life')
        BG = get_data(t, 'Fulfil BG Life')
        CL = get_data(t, 'Fulfil CL Life')
        SFD = get_data(t, 'Fulfil SF Direct Life')
        NMD = get_data(t, 'Fulfil NM Direct Life')
        NOD = get_data(t, 'Fulfil NO Direct Life')
        CLD = get_data(t, 'Fulfil CL Direct Life')
        itr = range(1, len(SF) + 1)

        #plt.plot(itr, Class, label="Total")
        plt.plot(itr, SF, label="Peasants Total")
        plt.plot(itr, NM, label="Nomads Total")
        plt.plot(itr, NO, label="Nobles Total")
        plt.plot(itr, CL, label="Clergy Total")
        plt.plot(itr, RE, label="Residents")
        plt.plot(itr, BG, label="Burghers")
        plt.plot(itr, SFD, label="Peasants Direct")
        plt.plot(itr, NMD, label="Nomads Direct")
        plt.plot(itr, NOD, label="Nobles Direct")
        plt.plot(itr, CLD, label="Clergy Direct")

def graphFulfill_Luxury(t, plt):
        "Luxury Needs Fulfillment"
        #Class = get_data(t, 'Class Pop')
        SF = get_data(t, 'Fulfil SF Luxury')
        NM = get_data(t, 'Fulfil NM Luxury')
        RE = get_data(t, 'Fulfil RE Luxury')
        NO = get_data(t, 'Fulfil NO Luxury')
        BG = get_data(t, 'Fulfil BG Luxury')
        CL = get_data(t, 'Fulfil CL Luxury')
        itr = range(1, len(SF) + 1)

        #plt.plot(itr, Class, label="Total")
        plt.plot(itr, SF, label="Peasants")
        plt.plot(itr, NM, label="Nomads")
        plt.plot(itr, NO, label="Nobles")
        plt.plot(itr, CL, label="Clergy")
        plt.plot(itr, RE, label="Residents")
        plt.plot(itr, BG, label="Burghers")

def graphGrowth_Rates_All(t, plt):
        "Yearly Growth Rates (All Classes)"
        formatter = FuncFormatter(to_percent)

        SF = get_data(t, 'Peasant Pop Total')
        NM = get_data(t, 'Nomads Pop Total')
        RE = get_data(t, 'Residents Pop Total')
        NO = get_data(t, 'Nobles Pop Total')
        BG = get_data(t, 'Burghers Pop Total')
        CL = get_data(t, 'Clergy Pop Total')

        SF_gr = [y / x - 1 for x, y in zip(SF[:-1], SF[1:])]
        NM_gr = [y / x - 1 for x, y in zip(NM[:-1], NM[1:])]
        RE_gr = [y / x - 1 for x, y in zip(RE[:-1], RE[1:])]
        NO_gr = [y / x - 1 for x, y in zip(NO[:-1], NO[1:])]
        BG_gr = [y / x - 1 for x, y in zip(BG[:-1], BG[1:])]
        CL_gr = [y / x - 1 for x, y in zip(CL[:-1], CL[1:])]

        itr = range(1, len(SF_gr) + 1)

        plt.plot(itr, SF_gr, label="Peasants")
        plt.plot(itr, NM_gr, label="Nomads")
        plt.plot(itr, RE_gr, label="Residents")
        plt.plot(itr, NO_gr, label="Nobles")
        plt.plot(itr, BG_gr, label="Burghers")
        plt.plot(itr, CL_gr, label="Clergy")
        plt.yaxis.set_major_formatter(formatter)

def graphGrowth_Rates_Elite(t, plt):
        "Yearly Growth Rates (Elites)"
        formatter = FuncFormatter(to_percent)

        NO = get_data(t, 'Nobles Pop Total')
        BG = get_data(t, 'Burghers Pop Total')
        CL = get_data(t, 'Clergy Pop Total')

        NO_gr = [y / x - 1 for x, y in zip(NO[:-1], NO[1:])]
        BG_gr = [y / x - 1 for x, y in zip(BG[:-1], BG[1:])]
        CL_gr = [y / x - 1 for x, y in zip(CL[:-1], CL[1:])]


        itr = range(1, len(NO_gr) + 1)

        plt.plot(itr, NO_gr, label="Nobles")
        plt.plot(itr, BG_gr, label="Burghers")
        plt.plot(itr, CL_gr, label="Clergy")
        plt.yaxis.set_major_formatter(formatter)

def graphGrowth_Rates_Rural(t, plt):
        "Yearly Growth Rates (Rurals)"
        formatter = FuncFormatter(to_percent)

        SF = get_data(t, 'Peasant Pop Total')
        NM = get_data(t, 'Nomads Pop Total')

        SF_gr = [y / x - 1 for x, y in zip(SF[:-1], SF[1:])]
        NM_gr = [y / x - 1 for x, y in zip(NM[:-1], NM[1:])]

        itr = range(1, len(SF_gr) + 1)

        plt.plot(itr, SF_gr, label="Peasants")
        plt.plot(itr, NM_gr, label="Nomads")
        plt.yaxis.set_major_formatter(formatter)

def graphGrowth_Rates_Urban(t, plt):
        "Yearly Growth Rates (Urbans)"
        formatter = FuncFormatter(to_percent)

        RE = get_data(t, 'Residents Pop Total')

        RE_gr = [y / x - 1 for x, y in zip(RE[:-1], RE[1:])]

        itr = range(1, len(RE_gr) + 1)

        plt.plot(itr, RE_gr, label="Residents")
        plt.yaxis.set_major_formatter(formatter)

def graphTotal_Pop_All(t, plt):
        "Total Population (All Classes)"
        #Class = get_data(t, 'Class Pop Total')
        SF = get_data(t, 'Peasant Pop Total')
        NM = get_data(t, 'Nomads Pop Total')
        RE = get_data(t, 'Residents Pop Total')
        NO = get_data(t, 'Nobles Pop Total')
        BG = get_data(t, 'Burghers Pop Total')
        CL = get_data(t, 'Clergy Pop Total')
        # BU = get_data(t, 'Literati Pop Total')
        itr = range(1, len(SF) + 1)

        #plt.plot(itr, Class, label="Total")
        plt.plot(itr, SF, label="Peasants")
        plt.plot(itr, NM, label="Nomads")
        plt.plot(itr, RE, label="Residents")
        plt.plot(itr, NO, label="Nobles")
        plt.plot(itr, BG, label="Burghers")
        plt.plot(itr, CL, label="Clergy")
        #plt.plot(itr, BU, label="Literati")

def graphTotal_Pop_Elite(t, plt):
        "Total Population (Elites)"
        #Class = get_data(t, 'Class Pop Total')
        NO = get_data(t, 'Nobles Pop Total')
        BG = get_data(t, 'Burghers Pop Total')
        CL = get_data(t, 'Clergy Pop Total')
        itr = range(1, len(NO) + 1)

        #plt.plot(itr, Class, label="Total")
        plt.plot(itr, NO, label="Nobles")
        plt.plot(itr, BG, label="Burghers")
        plt.plot(itr, CL, label="Clergy")

def graphTotal_Pop_Nomad(t, plt):
        "Total Population (Nomads)"
        #Class = get_data(t, 'Class Pop Total')
        NM = get_data(t, 'Nomads Pop Total')
        itr = range(1, len(NM) + 1)

        #plt.plot(itr, Class, label="Total")
        plt.plot(itr, NM, label="Nomads")

def graphTotal_Pop_Peasant(t, plt):
        "Total Population (Peasants)"
        #Class = get_data(t, 'Class Pop Total')
        SF = get_data(t, 'Peasant Pop Total')
        itr = range(1, len(SF) + 1)

        #plt.plot(itr, Class, label="Total")
        plt.plot(itr, SF, label="Peasants")

def graphTotal_Pop_Urban(t, plt):
        "Total Population (Urbans)"
        #Class = get_data(t, 'Class Pop Total')
        RE = get_data(t, 'Residents Pop Total')
        itr = range(1, len(RE) + 1)

        #plt.plot(itr, Class, label="Total")
        plt.plot(itr, RE, label="Residents")

def graphTotal_World(t, plt):
        "Total Population (World)"
        Class = get_data(t, 'Class Pop Total')

        itr = range(1, len(Class) + 1)

        plt.plot(itr, Class, label="Total")

def graphUrbanization(t, plt):
        "Urbanization Rate"
        formatter = FuncFormatter(to_percent)

        SF = get_data(t, 'Peasant Pop Total')
        NM = get_data(t, 'Nomads Pop Total')
        RE = get_data(t, 'Residents Pop Total')


        lower_classes = [a + b for a, b in zip(NM, SF)]
        urbanization = [a / b for a, b in zip(RE, lower_classes)]

        itr = range(1, len(urbanization) + 1)

        plt.plot(itr, urbanization, label="Urbanization Rate - RE/(SF+NM)")
        plt.yaxis.set_major_formatter(formatter)

def graphPrice_Cairo(t, plt):
        "Prices (Cairo)"
        food1 = get_data(t, 'Cairo Food Price')
        food2 = get_data(t, 'Cairo Salt Price')
        food3 = get_data(t, 'Cairo Fiber Price')
        food4 = get_data(t, 'Cairo Fuel Price')
        food5 = get_data(t, 'Cairo Raw Material Price')
        food6 = get_data(t, 'Cairo Exotics Price')
        food7 = get_data(t, 'Cairo Delicacies Price')
        food8 = get_data(t, 'Cairo Naval Product Price')
        itr = range(1, len(food1) + 1)

        plt.plot(itr, food1, label="Food")
        plt.plot(itr, food2, label="Salt")
        plt.plot(itr, food3, label="Fiber")
        plt.plot(itr, food4, label="Fuel")
        plt.plot(itr, food5, label="Raw")
        plt.plot(itr, food6, label="Exotics")
        plt.plot(itr, food7, label="Delicacies")
        plt.plot(itr, food8, label="Naval")

def graphPrice_Cuzco(t, plt):
        "Prices (Cuzco)"
        food1 = get_data(t, 'Cusco Food Price')
        food2 = get_data(t, 'Cusco Salt Price')
        food3 = get_data(t, 'Cusco Fiber Price')
        food4 = get_data(t, 'Cusco Fuel Price')
        food5 = get_data(t, 'Cusco Raw Material Price')
        food6 = get_data(t, 'Cusco Exotics Price')
        food7 = get_data(t, 'Cusco Delicacies Price')
        food8 = get_data(t, 'Cusco Naval Product Price')
        itr = range(1, len(food1) + 1)

        plt.plot(itr, food1, label="Food")
        plt.plot(itr, food2, label="Salt")
        plt.plot(itr, food3, label="Fiber")
        plt.plot(itr, food4, label="Fuel")
        plt.plot(itr, food5, label="Raw")
        plt.plot(itr, food6, label="Exotics")
        plt.plot(itr, food7, label="Delicacies")
        plt.plot(itr, food8, label="Naval")

def graphPrice_Delhi(t, plt):
        "Prices (Delhi)"
        food1 = get_data(t, 'Delhi Food Price')
        food2 = get_data(t, 'Delhi Salt Price')
        food3 = get_data(t, 'Delhi Fiber Price')
        food4 = get_data(t, 'Delhi Fuel Price')
        food5 = get_data(t, 'Delhi Raw Material Price')
        food6 = get_data(t, 'Delhi Exotics Price')
        food7 = get_data(t, 'Delhi Delicacies Price')
        food8 = get_data(t, 'Delhi Naval Product Price')
        itr = range(1, len(food1) + 1)

        plt.plot(itr, food1, label="Food")
        plt.plot(itr, food2, label="Salt")
        plt.plot(itr, food3, label="Fiber")
        plt.plot(itr, food4, label="Fuel")
        plt.plot(itr, food5, label="Raw")
        plt.plot(itr, food6, label="Exotics")
        plt.plot(itr, food7, label="Delicacies")
        plt.plot(itr, food8, label="Naval")

def graphPrice_Goa(t, plt):
        "Prices (Goa)"
        food1 = get_data(t, 'Gao Food Price')
        food2 = get_data(t, 'Gao Salt Price')
        food3 = get_data(t, 'Gao Fiber Price')
        food4 = get_data(t, 'Gao Fuel Price')
        food5 = get_data(t, 'Gao Raw Material Price')
        food6 = get_data(t, 'Gao Exotics Price')
        food7 = get_data(t, 'Gao Delicacies Price')
        food8 = get_data(t, 'Gao Naval Product Price')
        itr = range(1, len(food1) + 1)

        plt.plot(itr, food1, label="Food")
        plt.plot(itr, food2, label="Salt")
        plt.plot(itr, food3, label="Fiber")
        plt.plot(itr, food4, label="Fuel")
        plt.plot(itr, food5, label="Raw")
        plt.plot(itr, food6, label="Exotics")
        plt.plot(itr, food7, label="Delicacies")
        plt.plot(itr, food8, label="Naval")

def graphPrice_Delicacies(t, plt):
        "Price points of Delicacies"
        Delicacies1 = get_data(t, 'Paris Delicacies Price')
        Delicacies2 = get_data(t, 'Moscow Delicacies Price')
        Delicacies3 = get_data(t, 'Cairo Delicacies Price')
        Delicacies4 = get_data(t, 'Gao Delicacies Price')
        Delicacies5 = get_data(t, 'Mogadishu Delicacies Price')
        Delicacies6 = get_data(t, 'Delhi Delicacies Price')
        Delicacies7 = get_data(t, 'Malacca Delicacies Price')
        Delicacies8 = get_data(t, 'Nanking Delicacies Price')
        Delicacies9 = get_data(t, 'Mexico Delicacies Price')
        Delicacies10 = get_data(t, 'Cusco Delicacies Price')
        itr = range(1, len(Delicacies1) + 1)

        plt.plot(itr, Delicacies1, label="Paris")
        plt.plot(itr, Delicacies2, label="Moscow")
        plt.plot(itr, Delicacies3, label="Cairo")
        plt.plot(itr, Delicacies4, label="Goa")
        plt.plot(itr, Delicacies5, label="Mogadishu")
        plt.plot(itr, Delicacies6, label="Delhi")
        plt.plot(itr, Delicacies7, label="Malacca")
        plt.plot(itr, Delicacies8, label="Nanking")
        plt.plot(itr, Delicacies9, label="Mexico")
        plt.plot(itr, Delicacies10, label="Cuzco")

def graphPrice_Exotics(t, plt):
        "Price points of Exotics"
        Exotics1 = get_data(t, 'Paris Exotics Price')
        Exotics2 = get_data(t, 'Moscow Exotics Price')
        Exotics3 = get_data(t, 'Cairo Exotics Price')
        Exotics4 = get_data(t, 'Gao Exotics Price')
        Exotics5 = get_data(t, 'Mogadishu Exotics Price')
        Exotics6 = get_data(t, 'Delhi Exotics Price')
        Exotics7 = get_data(t, 'Malacca Exotics Price')
        Exotics8 = get_data(t, 'Nanking Exotics Price')
        Exotics9 = get_data(t, 'Mexico Exotics Price')
        Exotics10 = get_data(t, 'Cusco Exotics Price')
        itr = range(1, len(Exotics1) + 1)

        plt.plot(itr, Exotics1, label="Paris")
        plt.plot(itr, Exotics2, label="Moscow")
        plt.plot(itr, Exotics3, label="Cairo")
        plt.plot(itr, Exotics4, label="Goa")
        plt.plot(itr, Exotics5, label="Mogadishu")
        plt.plot(itr, Exotics6, label="Delhi")
        plt.plot(itr, Exotics7, label="Malacca")
        plt.plot(itr, Exotics8, label="Nanking")
        plt.plot(itr, Exotics9, label="Mexico")
        plt.plot(itr, Exotics10, label="Cuzco")

def graphPrice_Fiber(t, plt):
        "Price points of Fiber"
        Fiber1 = get_data(t, 'Paris Fiber Price')
        Fiber2 = get_data(t, 'Moscow Fiber Price')
        Fiber3 = get_data(t, 'Cairo Fiber Price')
        Fiber4 = get_data(t, 'Gao Fiber Price')
        Fiber5 = get_data(t, 'Mogadishu Fiber Price')
        Fiber6 = get_data(t, 'Delhi Fiber Price')
        Fiber7 = get_data(t, 'Malacca Fiber Price')
        Fiber8 = get_data(t, 'Nanking Fiber Price')
        Fiber9 = get_data(t, 'Mexico Fiber Price')
        Fiber10 = get_data(t, 'Cusco Fiber Price')
        itr = range(1, len(Fiber1) + 1)

        plt.plot(itr, Fiber1, label="Paris")
        plt.plot(itr, Fiber2, label="Moscow")
        plt.plot(itr, Fiber3, label="Cairo")
        plt.plot(itr, Fiber4, label="Goa")
        plt.plot(itr, Fiber5, label="Mogadishu")
        plt.plot(itr, Fiber6, label="Delhi")
        plt.plot(itr, Fiber7, label="Malacca")
        plt.plot(itr, Fiber8, label="Nanking")
        plt.plot(itr, Fiber9, label="Mexico")
        plt.plot(itr, Fiber10, label="Cuzco")

def graphPrice_Food(t, plt):
        "Price points of Food"
        food1 = get_data(t, 'Paris Food Price')
        food2 = get_data(t, 'Moscow Food Price')
        food3 = get_data(t, 'Cairo Food Price')
        food4 = get_data(t, 'Gao Food Price')
        food5 = get_data(t, 'Mogadishu Food Price')
        food6 = get_data(t, 'Delhi Food Price')
        food7 = get_data(t, 'Malacca Food Price')
        food8 = get_data(t, 'Nanking Food Price')
        food9 = get_data(t, 'Mexico Food Price')
        food10 = get_data(t, 'Cusco Food Price')
        itr = range(1, len(food1) + 1)

        plt.plot(itr, food1, label="Paris")
        plt.plot(itr, food2, label="Moscow")
        plt.plot(itr, food3, label="Cairo")
        plt.plot(itr, food4, label="Goa")
        plt.plot(itr, food5, label="Mogadishu")
        plt.plot(itr, food6, label="Delhi")
        plt.plot(itr, food7, label="Malacca")
        plt.plot(itr, food8, label="Nanking")
        plt.plot(itr, food9, label="Mexico")
        plt.plot(itr, food10, label="Cuzco")

def graphPrice_Fuel(t, plt):
        "Price points of Fuel"
        Fuel1 = get_data(t, 'Paris Fuel Price')
        Fuel2 = get_data(t, 'Moscow Fuel Price')
        Fuel3 = get_data(t, 'Cairo Fuel Price')
        Fuel4 = get_data(t, 'Gao Fuel Price')
        Fuel5 = get_data(t, 'Mogadishu Fuel Price')
        Fuel6 = get_data(t, 'Delhi Fuel Price')
        Fuel7 = get_data(t, 'Malacca Fuel Price')
        Fuel8 = get_data(t, 'Nanking Fuel Price')
        Fuel9 = get_data(t, 'Mexico Fuel Price')
        Fuel10 = get_data(t, 'Cusco Fuel Price')
        itr = range(1, len(Fuel1) + 1)

        plt.plot(itr, Fuel1, label="Paris")
        plt.plot(itr, Fuel2, label="Moscow")
        plt.plot(itr, Fuel3, label="Cairo")
        plt.plot(itr, Fuel4, label="Goa")
        plt.plot(itr, Fuel5, label="Mogadishu")
        plt.plot(itr, Fuel6, label="Delhi")
        plt.plot(itr, Fuel7, label="Malacca")
        plt.plot(itr, Fuel8, label="Nanking")
        plt.plot(itr, Fuel9, label="Mexico")
        plt.plot(itr, Fuel10, label="Cuzco")

def graphPrice_Naval(t, plt):
        "Price points of Naval"
        Naval1 = get_data(t, 'Paris Naval Product Price')
        Naval2 = get_data(t, 'Moscow Naval Product Price')
        Naval3 = get_data(t, 'Cairo Naval Product Price')
        Naval4 = get_data(t, 'Gao Naval Product Price')
        Naval5 = get_data(t, 'Mogadishu Naval Product Price')
        Naval6 = get_data(t, 'Delhi Naval Product Price')
        Naval7 = get_data(t, 'Malacca Naval Product Price')
        Naval8 = get_data(t, 'Nanking Naval Product Price')
        Naval9 = get_data(t, 'Mexico Naval Product Price')
        Naval10 = get_data(t, 'Cusco Naval Product Price')
        itr = range(1, len(Naval1) + 1)

        plt.plot(itr, Naval1, label="Paris")
        plt.plot(itr, Naval2, label="Moscow")
        plt.plot(itr, Naval3, label="Cairo")
        plt.plot(itr, Naval4, label="Goa")
        plt.plot(itr, Naval5, label="Mogadishu")
        plt.plot(itr, Naval6, label="Delhi")
        plt.plot(itr, Naval7, label="Malacca")
        plt.plot(itr, Naval8, label="Nanking")
        plt.plot(itr, Naval9, label="Mexico")
        plt.plot(itr, Naval10, label="Cuzco")

def graphPrice_Raw(t, plt):
        "Price points of Raw"
        Raw1 = get_data(t, 'Paris Raw Material Price')
        Raw2 = get_data(t, 'Moscow Raw Material Price')
        Raw3 = get_data(t, 'Cairo Raw Material Price')
        Raw4 = get_data(t, 'Gao Raw Material Price')
        Raw5 = get_data(t, 'Mogadishu Raw Material Price')
        Raw6 = get_data(t, 'Delhi Raw Material Price')
        Raw7 = get_data(t, 'Malacca Raw Material Price')
        Raw8 = get_data(t, 'Nanking Raw Material Price')
        Raw9 = get_data(t, 'Mexico Raw Material Price')
        Raw10 = get_data(t, 'Cusco Raw Material Price')
        itr = range(1, len(Raw1) + 1)

        plt.plot(itr, Raw1, label="Paris")
        plt.plot(itr, Raw2, label="Moscow")
        plt.plot(itr, Raw3, label="Cairo")
        plt.plot(itr, Raw4, label="Goa")
        plt.plot(itr, Raw5, label="Mogadishu")
        plt.plot(itr, Raw6, label="Delhi")
        plt.plot(itr, Raw7, label="Malacca")
        plt.plot(itr, Raw8, label="Nanking")
        plt.plot(itr, Raw9, label="Mexico")
        plt.plot(itr, Raw10, label="Cuzco")

def graphPrice_Salt(t, plt):
        "Price points of Salt"
        Salt1 = get_data(t, 'Paris Salt Price')
        Salt2 = get_data(t, 'Moscow Salt Price')
        Salt3 = get_data(t, 'Cairo Salt Price')
        Salt4 = get_data(t, 'Gao Salt Price')
        Salt5 = get_data(t, 'Mogadishu Salt Price')
        Salt6 = get_data(t, 'Delhi Salt Price')
        Salt7 = get_data(t, 'Malacca Salt Price')
        Salt8 = get_data(t, 'Nanking Salt Price')
        Salt9 = get_data(t, 'Mexico Salt Price')
        Salt10 = get_data(t, 'Cusco Salt Price')
        itr = range(1, len(Salt1) + 1)

        plt.plot(itr, Salt1, label="Paris")
        plt.plot(itr, Salt2, label="Moscow")
        plt.plot(itr, Salt3, label="Cairo")
        plt.plot(itr, Salt4, label="Goa")
        plt.plot(itr, Salt5, label="Mogadishu")
        plt.plot(itr, Salt6, label="Delhi")
        plt.plot(itr, Salt7, label="Malacca")
        plt.plot(itr, Salt8, label="Nanking")
        plt.plot(itr, Salt9, label="Mexico")
        plt.plot(itr, Salt10, label="Cuzco")

def graphPrice_Malacca(t, plt):
        "Prices (Malacca)"
        food1 = get_data(t, 'Malacca Food Price')
        food2 = get_data(t, 'Malacca Salt Price')
        food3 = get_data(t, 'Malacca Fiber Price')
        food4 = get_data(t, 'Malacca Fuel Price')
        food5 = get_data(t, 'Malacca Raw Material Price')
        food6 = get_data(t, 'Malacca Exotics Price')
        food7 = get_data(t, 'Malacca Delicacies Price')
        food8 = get_data(t, 'Malacca Naval Product Price')
        itr = range(1, len(food1) + 1)

        plt.plot(itr, food1, label="Food")
        plt.plot(itr, food2, label="Salt")
        plt.plot(itr, food3, label="Fiber")
        plt.plot(itr, food4, label="Fuel")
        plt.plot(itr, food5, label="Raw")
        plt.plot(itr, food6, label="Exotics")
        plt.plot(itr, food7, label="Delicacies")
        plt.plot(itr, food8, label="Naval")

def graphPrice_Mexico(t, plt):
        "Prices (Mexico)"
        food1 = get_data(t, 'Mexico Food Price')
        food2 = get_data(t, 'Mexico Salt Price')
        food3 = get_data(t, 'Mexico Fiber Price')
        food4 = get_data(t, 'Mexico Fuel Price')
        food5 = get_data(t, 'Mexico Raw Material Price')
        food6 = get_data(t, 'Mexico Exotics Price')
        food7 = get_data(t, 'Mexico Delicacies Price')
        food8 = get_data(t, 'Mexico Naval Product Price')
        itr = range(1, len(food1) + 1)

        plt.plot(itr, food1, label="Food")
        plt.plot(itr, food2, label="Salt")
        plt.plot(itr, food3, label="Fiber")
        plt.plot(itr, food4, label="Fuel")
        plt.plot(itr, food5, label="Raw")
        plt.plot(itr, food6, label="Exotics")
        plt.plot(itr, food7, label="Delicacies")
        plt.plot(itr, food8, label="Naval")

def graphPrice_Mogadishu(t, plt):
        "Prices (Mogadishu)"
        food1 = get_data(t, 'Mogadishu Food Price')
        food2 = get_data(t, 'Mogadishu Salt Price')
        food3 = get_data(t, 'Mogadishu Fiber Price')
        food4 = get_data(t, 'Mogadishu Fuel Price')
        food5 = get_data(t, 'Mogadishu Raw Material Price')
        food6 = get_data(t, 'Mogadishu Exotics Price')
        food7 = get_data(t, 'Mogadishu Delicacies Price')
        food8 = get_data(t, 'Mogadishu Naval Product Price')
        itr = range(1, len(food1) + 1)

        plt.plot(itr, food1, label="Food")
        plt.plot(itr, food2, label="Salt")
        plt.plot(itr, food3, label="Fiber")
        plt.plot(itr, food4, label="Fuel")
        plt.plot(itr, food5, label="Raw")
        plt.plot(itr, food6, label="Exotics")
        plt.plot(itr, food7, label="Delicacies")
        plt.plot(itr, food8, label="Naval")

def graphPrice_Moscow(t, plt):
        "Prices (Moscow)"
        food1 = get_data(t, 'Moscow Food Price')
        food2 = get_data(t, 'Moscow Salt Price')
        food3 = get_data(t, 'Moscow Fiber Price')
        food4 = get_data(t, 'Moscow Fuel Price')
        food5 = get_data(t, 'Moscow Raw Material Price')
        food6 = get_data(t, 'Moscow Exotics Price')
        food7 = get_data(t, 'Moscow Delicacies Price')
        food8 = get_data(t, 'Moscow Naval Product Price')
        itr = range(1, len(food1) + 1)

        plt.plot(itr, food1, label="Food")
        plt.plot(itr, food2, label="Salt")
        plt.plot(itr, food3, label="Fiber")
        plt.plot(itr, food4, label="Fuel")
        plt.plot(itr, food5, label="Raw")
        plt.plot(itr, food6, label="Exotics")
        plt.plot(itr, food7, label="Delicacies")
        plt.plot(itr, food8, label="Naval")

def graphPrice_Nanking(t, plt):
        "Prices (Nanking)"
        food1 = get_data(t, 'Nanking Food Price')
        food2 = get_data(t, 'Nanking Salt Price')
        food3 = get_data(t, 'Nanking Fiber Price')
        food4 = get_data(t, 'Nanking Fuel Price')
        food5 = get_data(t, 'Nanking Raw Material Price')
        food6 = get_data(t, 'Nanking Exotics Price')
        food7 = get_data(t, 'Nanking Delicacies Price')
        food8 = get_data(t, 'Nanking Naval Product Price')
        itr = range(1, len(food1) + 1)

        plt.plot(itr, food1, label="Food")
        plt.plot(itr, food2, label="Salt")
        plt.plot(itr, food3, label="Fiber")
        plt.plot(itr, food4, label="Fuel")
        plt.plot(itr, food5, label="Raw")
        plt.plot(itr, food6, label="Exotics")
        plt.plot(itr, food7, label="Delicacies")
        plt.plot(itr, food8, label="Naval")

def graphPrice_Paris(t, plt):
        "Prices (Paris)"
        food1 = get_data(t, 'Paris Food Price')
        food2 = get_data(t, 'Paris Salt Price')
        food3 = get_data(t, 'Paris Fiber Price')
        food4 = get_data(t, 'Paris Fuel Price')
        food5 = get_data(t, 'Paris Raw Material Price')
        food6 = get_data(t, 'Paris Exotics Price')
        food7 = get_data(t, 'Paris Delicacies Price')
        food8 = get_data(t, 'Paris Naval Product Price')
        itr = range(1, len(food1) + 1)

        plt.plot(itr, food1, label="Food")
        plt.plot(itr, food2, label="Salt")
        plt.plot(itr, food3, label="Fiber")
        plt.plot(itr, food4, label="Fuel")
        plt.plot(itr, food5, label="Raw")
        plt.plot(itr, food6, label="Exotics")
        plt.plot(itr, food7, label="Delicacies")
        plt.plot(itr, food8, label="Naval")

def graphProd_Diff(t, plt):
        "<please check this>"
        food = get_data(t, 'Food Production')
        salt = get_data(t, 'Salt Production')
        fiber = get_data(t, 'Fiber Production')
        fuel = get_data(t, 'Fuel Production')
        raw = get_data(t, 'Raw Material Production')
        delicacies = get_data(t, 'Delicacies Production')
        exotic = get_data(t, 'Exotics Production')
        consumer = get_data(t, 'Consumer Product Production')
        military = get_data(t, 'Military Product Production')
        naval = get_data(t, 'Naval Product Production')
        industrial = get_data(t, 'Industrial Product Production')
        luxury = get_data(t, 'Luxury Product Production')
        knowledge = get_data(t, 'Knowledge Production')
        food2 = get_data(t, 'Food Demand')
        salt2 = get_data(t, 'Salt Demand')
        fiber2 = get_data(t, 'Fiber Demand')
        fuel2 = get_data(t, 'Fuel Demand')
        raw2 = get_data(t, 'Raw Material Demand')
        delicacies2 = get_data(t, 'Delicacies Demand')
        exotic2 = get_data(t, 'Exotics Demand')
        consumer2 = get_data(t, 'Consumer Product Demand')
        military2 = get_data(t, 'Military Product Demand')
        naval2 = get_data(t, 'Naval Product Demand')
        industrial2 = get_data(t, 'Industrial Product Demand')
        luxury2 = get_data(t, 'Luxury Product Demand')
        knowledge2 = get_data(t, 'Knowledge Demand')
        food3 = get_data(t, 'Food DirectBuy')
        salt3 = get_data(t, 'Salt DirectBuy')
        fiber3 = get_data(t, 'Fiber DirectBuy')
        fuel3 = get_data(t, 'Fuel DirectBuy')
        food = food + food3
        salt = salt + salt3
        fiber = fiber + fiber3
        fuel = fuel + fuel3
        food2 = food2 + food3
        salt2 = salt2 + salt3
        fiber2 = fiber2 + fiber3
        fuel2 = fuel2 + fuel3
        itr = range(1, len(food) + 1)
        food = [food[i]-food2[i] for i in range(len(food))]
        salt = [salt[i]-salt2[i] for i in range(len(salt))]
        fiber = [fiber[i]-fiber2[i] for i in range(len(fiber))]
        fuel = [fuel[i]-fuel2[i] for i in range(len(fuel))]
        raw = [raw[i]-raw2[i] for i in range(len(raw))]
        delicacies = [delicacies[i]-delicacies2[i] for i in range(len(delicacies))]
        exotic = [exotic[i]-exotic2[i] for i in range(len(exotic))]
        consumer = [consumer[i]-consumer2[i] for i in range(len(consumer))]
        military = [military[i]-military2[i] for i in range(len(military))]
        naval = [naval[i]-naval2[i] for i in range(len(naval))]
        industrial = [industrial[i]-industrial2[i] for i in range(len(industrial))]
        luxury = [luxury[i]-luxury2[i] for i in range(len(luxury))]
        knowledge = [knowledge[i]-knowledge2[i] for i in range(len(knowledge))]

        plt.plot(itr, food, label="Food")
        plt.plot(itr, salt, label="Salt")
        plt.plot(itr, fiber, label="Fiber")
        plt.plot(itr, fuel, label="Fuel")
        plt.plot(itr, raw, label="Raw")
        plt.plot(itr, delicacies, label="Delicacies")
        plt.plot(itr, exotic, label="Exotics")
        plt.plot(itr, consumer, label="Consumer")
        plt.plot(itr, military, label="Military")
        plt.plot(itr, naval, label="Naval")
        plt.plot(itr, industrial, label="Industrial")
        plt.plot(itr, luxury, label="Luxury")
        plt.plot(itr, knowledge, label="Knowledge")

def graphProd_Diff_Foodless(t, plt):
        "<please check this>"
        # food = get_data(t, 'Food Production')
        salt = get_data(t, 'Salt Production')
        fiber = get_data(t, 'Fiber Production')
        fuel = get_data(t, 'Fuel Production')
        raw = get_data(t, 'Raw Material Production')
        delicacies = get_data(t, 'Delicacies Production')
        exotic = get_data(t, 'Exotics Production')
        consumer = get_data(t, 'Consumer Product Production')
        military = get_data(t, 'Military Product Production')
        naval = get_data(t, 'Naval Product Production')
        industrial = get_data(t, 'Industrial Product Production')
        luxury = get_data(t, 'Luxury Product Production')
        knowledge = get_data(t, 'Knowledge Production')
        # food2 = get_data(t, 'Food Demand')
        salt2 = get_data(t, 'Salt Demand')
        fiber2 = get_data(t, 'Fiber Demand')
        fuel2 = get_data(t, 'Fuel Demand')
        raw2 = get_data(t, 'Raw Material Demand')
        delicacies2 = get_data(t, 'Delicacies Demand')
        exotic2 = get_data(t, 'Exotics Demand')
        consumer2 = get_data(t, 'Consumer Product Demand')
        military2 = get_data(t, 'Military Product Demand')
        naval2 = get_data(t, 'Naval Product Demand')
        industrial2 = get_data(t, 'Industrial Product Demand')
        luxury2 = get_data(t, 'Luxury Product Demand')
        knowledge2 = get_data(t, 'Knowledge Demand')
        # food3 = get_data(t, 'Food DirectBuy')
        salt3 = get_data(t, 'Salt DirectBuy')
        fiber3 = get_data(t, 'Fiber DirectBuy')
        fuel3 = get_data(t, 'Fuel DirectBuy')
        # food = food + food3
        salt = salt + salt3
        fiber = fiber + fiber3
        fuel = fuel + fuel3
        # food2 = food2 + food3
        salt2 = salt2 + salt3
        fiber2 = fiber2 + fiber3
        fuel2 = fuel2 + fuel3
        itr = range(1, len(salt) + 1)
        # food = [food[i]-food2[i] for i in range(len(food))]
        salt = [salt[i]-salt2[i] for i in range(len(salt))]
        fiber = [fiber[i]-fiber2[i] for i in range(len(fiber))]
        fuel = [fuel[i]-fuel2[i] for i in range(len(fuel))]
        raw = [raw[i]-raw2[i] for i in range(len(raw))]
        delicacies = [delicacies[i]-delicacies2[i] for i in range(len(delicacies))]
        exotic = [exotic[i]-exotic2[i] for i in range(len(exotic))]
        consumer = [consumer[i]-consumer2[i] for i in range(len(consumer))]
        military = [military[i]-military2[i] for i in range(len(military))]
        naval = [naval[i]-naval2[i] for i in range(len(naval))]
        industrial = [industrial[i]-industrial2[i] for i in range(len(industrial))]
        luxury = [luxury[i]-luxury2[i] for i in range(len(luxury))]
        knowledge = [knowledge[i]-knowledge2[i] for i in range(len(knowledge))]

        #plt.plot(itr, food, label="Food")
        plt.plot(itr, salt, label="Salt")
        plt.plot(itr, fiber, label="Fiber")
        plt.plot(itr, fuel, label="Fuel")
        plt.plot(itr, raw, label="Raw")
        plt.plot(itr, delicacies, label="Delicacies")
        plt.plot(itr, exotic, label="Exotics")
        plt.plot(itr, consumer, label="Consumer")
        plt.plot(itr, military, label="Military")
        plt.plot(itr, naval, label="Naval")
        plt.plot(itr, industrial, label="Industrial")
        plt.plot(itr, luxury, label="Luxury")
        plt.plot(itr, knowledge, label="Knowledge")

def graphProperty(t, plt):
        "Property Size"
        Agriculture = get_data(t, 'Building Agriculture Total')
        Forestry = get_data(t, 'Building Forestry Total')
        Extraction = get_data(t, 'Building Extraction Total')
        Fishery = get_data(t, 'Building Fishery Total')
        Industrial = get_data(t, 'Building Industrial Total')
        Commercial = get_data(t, 'Building Commercial Total')
        Academic = get_data(t, 'Building Academic Total')
        Rural = get_data(t, 'Building Rural Total')
        Urban = get_data(t, 'Building Urban Total')
        itr = range(1, len(Urban) + 1)

        plt.plot(itr, Rural, label="Rural", linestyle='--')
        plt.plot(itr, Urban, label="Urban", linestyle='--')
        plt.plot(itr, Agriculture, label="Agriculture")
        plt.plot(itr, Forestry, label="Forestry")
        plt.plot(itr, Extraction, label="Extraction")
        plt.plot(itr, Fishery, label="Fishery")
        plt.plot(itr, Industrial, label="Industrial")
        plt.plot(itr, Commercial, label="Commercial")
        plt.plot(itr, Academic, label="Academic")

def graphRaw(t, plt):
        "Raw Data"
        Fuelp = np.array(get_data(t, 'Raw Material Production'))
        Fueld = np.array(get_data(t, 'Raw Material Demand'))
        itr = range(1, len(Fuelp) + 1)

        plt.plot(itr, Fuelp, label="Production")
        plt.plot(itr, Fueld, label="Demand")

def graphRE_Income(t, plt):
        "Resident Income"
        Total = get_data(t, 'Resident Income Total')
        Innate = get_data(t, 'Resident Income Innate')
        Tax = get_data(t, 'Resident Income Tax')
        Property = get_data(t, 'Resident Income Property')
        Prod = get_data(t, 'Resident Income Prod')
        itr = range(1, len(Total) + 1)

        plt.plot(itr, Total, label="Total")
        plt.plot(itr, Innate, label="Innate")
        plt.plot(itr, Tax, label="Tax")
        plt.plot(itr, Property, label="Property")
        plt.plot(itr, Prod, label="Prod")

def graphSalt(t, plt):
        "Salt Data"
        Saltp = np.array(get_data(t, 'Salt Production'))
        Saltd = np.array(get_data(t, 'Salt Demand'))
        Salte = np.array(get_data(t, 'Salt DirectBuy'))
        Saltf = Saltd + Salte
        Saltj = Saltp + Salte
        itr = range(1, len(Saltp) + 1)

        plt.plot(itr, Saltp, label="Production")
        plt.plot(itr, Saltd, label="Market Demand")
        plt.plot(itr, Salte, label="Direct Buy")
        plt.plot(itr, Saltf, label="Total Demand")
        plt.plot(itr, Saltj, label="Total Production")

def graphSF_Income(t, plt):
        "Peasant Income"
        Total = get_data(t, 'Peasant Income Total')
        Innate = get_data(t, 'Peasant Income Innate')
        Tax = get_data(t, 'Peasant Income Tax')
        Property = get_data(t, 'Peasant Income Property')
        Prod = get_data(t, 'Peasant Income Prod')
        itr = range(1, len(Total) + 1)

        plt.plot(itr, Total, label="Total")
        plt.plot(itr, Innate, label="Innate")
        plt.plot(itr, Tax, label="Tax")
        plt.plot(itr, Property, label="Property")
        plt.plot(itr, Prod, label="Prod")

def graphSF_Spend(t, plt):
        "Peasant Spending"
        Total = get_data(t, 'Peasant Spend Total')
        Tax = get_data(t, 'Peasant Spend Tax')
        Property = get_data(t, 'Peasant Spend Property')
        #Infra = get_data(t, 'Peasant Spend Infra')
        Prod = get_data(t, 'Peasant Spend Prod')
        itr = range(1, len(Total) + 1)

        plt.plot(itr, Total, label="Total")
        plt.plot(itr, Tax, label="Tax")
        plt.plot(itr, Property, label="Property")
        #plt.plot(itr, Infra, label="Infra")
        plt.plot(itr, Prod, label="Prod")

def graphLeak_Test(t, plt):
        "Money Leakage"
        wealth = get_data(t, 'Prod Leak Test')
        wealth2 = get_data(t, 'Tax Leak Test')
        wealth3 = get_data(t, 'Expected Wealth Change')
        wealth4 = get_data(t, 'Expected Income Spend')
        wealth5 = get_data(t, 'Infra Leak Test')
        wealth6 = get_data(t, 'Tariff_Income')
        itr = range(1, len(wealth) + 1)

        #plt.plot(itr, wage, label="Total")
        plt.plot(itr, wealth, label="Prod Leak Test")
        plt.plot(itr, wealth2, label="Tax Leak Test")
        plt.plot(itr, wealth3, label="Expected Wealth Change")
        plt.plot(itr, wealth4, label="Expected Income Spend")
        plt.plot(itr, wealth5, label="Infra Leak Test")
        plt.plot(itr, wealth6, label="Tariff Income")

def graphTrade_Balance(t, plt):
        "Trade Balance"
        food1 = get_data(t, 'Trade Balance')
        itr = range(1, len(food1) + 1)

        plt.plot(itr, food1, label="Trade Balance")

def graphWages(t, plt):
        "Wages"
        food1 = get_data(t, 'Rural Wage')
        food2 = get_data(t, 'Nomad Wage')
        food3 = get_data(t, 'Urban Wage')
        itr = range(1, len(food1) + 1)

        plt.plot(itr, food1, label="Rural")
        plt.plot(itr, food2, label="Nomad")
        plt.plot(itr, food3, label="Urban")

def graphWealth_per_All(t, plt):
        "Wealth Per Capita (All Classes)"
        wealth_SF = get_data(t, 'Peasant Wealth')
        wealth_NM = get_data(t, 'Nomad Wealth')
        wealth_RE = get_data(t, 'Resident Wealth')
        wealth_NO = get_data(t, 'Noble Wealth')
        wealth_BG = get_data(t, 'Burgher Wealth')
        wealth_CL = get_data(t, 'Clergy Wealth')
        SF = get_data(t, 'Peasant Pop Total')
        NM = get_data(t, 'Nomads Pop Total')
        RE = get_data(t, 'Residents Pop Total')
        NO = get_data(t, 'Nobles Pop Total')
        BG = get_data(t, 'Burghers Pop Total')
        CL = get_data(t, 'Clergy Pop Total')

        SF_wpc = [a / b for a, b in zip(wealth_SF, SF)]
        NM_wpc = [a / b for a, b in zip(wealth_NM, NM)]
        RE_wpc = [a / b for a, b in zip(wealth_RE, RE)]
        NO_wpc = [a / b for a, b in zip(wealth_NO, NO)]
        BG_wpc = [a / b for a, b in zip(wealth_BG, BG)]
        CL_wpc = [a / b for a, b in zip(wealth_CL, CL)]
        itr = range(1, len(SF_wpc) + 1)

        plt.plot(itr, SF_wpc, label="Peasants Wealth p.c.")
        plt.plot(itr, NM_wpc, label="Nomads Wealth p.c.")
        plt.plot(itr, RE_wpc, label="Residents Wealth p.c.")
        plt.plot(itr, NO_wpc, label="Nobles Wealth p.c.")
        plt.plot(itr, BG_wpc, label="Burghers Wealth p.c.")
        plt.plot(itr, CL_wpc, label="Clergy Wealth p.c.")

def graphWealth_per_Elite(t, plt):
        "Wealth Per Capita (Elites)"
        wealth_NO = get_data(t, 'Noble Wealth')
        wealth_BG = get_data(t, 'Burgher Wealth')
        wealth_CL = get_data(t, 'Clergy Wealth')
        NO = get_data(t, 'Nobles Pop Total')
        BG = get_data(t, 'Burghers Pop Total')
        CL = get_data(t, 'Clergy Pop Total')

        NO_wpc = [a / b for a, b in zip(wealth_NO, NO)]
        BG_wpc = [a / b for a, b in zip(wealth_BG, BG)]
        CL_wpc = [a / b for a, b in zip(wealth_CL, CL)]
        itr = range(1, len(wealth_NO) + 1)

        plt.plot(itr, NO_wpc, label="Nobles Wealth p.c.")
        plt.plot(itr, BG_wpc, label="Burghers Wealth p.c.")
        plt.plot(itr, CL_wpc, label="Clergy Wealth p.c.")

def graphWealth_per_Lower(t, plt):
        "Wealth Per Capita (Lower Classes)"
        wealth_SF = get_data(t, 'Peasant Wealth')
        wealth_NM = get_data(t, 'Nomad Wealth')
        wealth_RE = get_data(t, 'Resident Wealth')
        SF = get_data(t, 'Peasant Pop Total')
        NM = get_data(t, 'Nomads Pop Total')
        RE = get_data(t, 'Residents Pop Total')

        SF_wpc = [a / b for a, b in zip(wealth_SF, SF)]
        NM_wpc = [a / b for a, b in zip(wealth_NM, NM)]
        RE_wpc = [a / b for a, b in zip(wealth_RE, RE)]
        itr = range(1, len(SF_wpc) + 1)

        plt.plot(itr, SF_wpc, label="Peasants Wealth p.c.")
        plt.plot(itr, NM_wpc, label="Nomads Wealth p.c.")
        plt.plot(itr, RE_wpc, label="Residents Wealth p.c.")

def graphWealth(t, plt):
        "Wealth"
        wealth = get_data(t, 'Total Wealth')
        wealth2 = get_data(t, 'Infra Wealth')
        itr = range(1, len(wealth) + 1)

        #plt.plot(itr, wage, label="Total")
        plt.plot(itr, wealth, label="Wealth")
        plt.plot(itr, wealth2, label="Infra Wealth")

def graphWealth_Change(t, plt):
        "Wealth Change"
        Innate = get_data(t, 'WealthChange Innate')
        Gold = get_data(t, 'WealthChange Gold')
        Property = get_data(t, 'WealthChange Property')
        Wages = get_data(t, 'WealthChange Wages')
        Infra = get_data(t, 'WealthChange Infra')
        Manpower = get_data(t, 'WealthChange Manpower')
        StateInc = get_data(t, 'WealthChange StateInc')
        ExtraTax = get_data(t, 'WealthChange ExtraTax')
        itr = range(1, len(Innate) + 1)

        plt.plot(itr, Innate, label="Innate")
        plt.plot(itr, Gold, label="Gold")
        plt.plot(itr, Property, label="BU Property")
        plt.plot(itr, Wages, label="Wages")
        plt.plot(itr, Infra, label="Infra")
        plt.plot(itr, Manpower, label="Manpower")
        plt.plot(itr, StateInc, label="State Income")
        plt.plot(itr, ExtraTax, label="Special Taxes")

if __name__ == "__main__":
    import MT_grapher
