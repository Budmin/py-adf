from lxml import etree
from iso4217 import Currency
from typing import Literal, List, Dict
from datetime import datetime

# a system that handles the creation, modification, and outputting of adf files




class Name:
  def __init__(self, value: str):
    self.value = value
    self.part = None
    self.type = None

  def set_part(self, part: Literal["first", "middle", "suffix", "last", "full"]):
    # NOTE: this is technically duplication. I think it's small enough to be fine, but it may need to be changed later.
    valid_parts = ["first", "middle", "suffix", "last", "full"] 

    if not part in valid_parts:
       raise ValueError("must have a valid part value")
    
    self.part = part
    return self
  
  def set_type(self, new_type: Literal["individual", "business"]):
    # NOTE: this is technically duplication. I think it's small enough to be fine, but it may need to be changed later.
    valid_types = ["individual", "business"]

    if not new_type in valid_types:
       raise ValueError("must have a valid type value")
    
    self.type = new_type
    return self


  def to_xml(self):
    elem = etree.Element("name")
    elem.text = self.value

    if self.part:
      elem.set("part", self.part)
    
    if self.type:
      elem.set("type", self.type)

    return elem
    

class Email:
  def __init__(self, value: str):
    # TODO: do we want to include any kind of email validation in this?
    self.value = value
    self.is_preferred_contact: bool | None = None

  def set_preferred_contact(self, new_value: bool | None):
    self.is_preferred_contact = new_value
    return self
  
  def to_xml(self):
    elem = etree.Element("email")
    elem.text = self.value

    if self.is_preferred_contact != None:
      elem.set("preferredcontact", str(int(self.is_preferred_contact)))
    
    return elem


class PhoneNumber:
  def __init__(self, value: str):
    self.value = value
    self.type = None
    self.time = None
    self.is_preferred_contact = None

  def set_type(self, new_type: Literal["phone", "fax", "cellphone", "pager"]):
    # NOTE: this is technically duplication. I think it's small enough to be fine but it may need to be changed later
    valid_types = ["phone", "fax", "cellphone", "pager"]

    if not new_type in valid_types:
      raise ValueError("must have a valid type value")

    self.type = new_type
    return self
  
  def set_time(self, new_time: Literal["morning", "afternoon", "evening", "nopreference", "day"]):
    # NOTE: this is technically duplication. I think it's small enough to be fine but it may need to be changed later
    valid_times = ["morning", "afternoon", "evening", "nopreference", "day"]

    if not new_time in valid_times:
      raise ValueError("must have a valid time")
  
    self.time = new_time
    return self
  
  def set_preferred_contact(self, new_value: bool | None):
    self.is_preferred_contact = new_value
    return self

  def to_xml(self):
    elem = etree.Element("phone")
    elem.text = self.value

    if self.type:
      elem.set("type", self.type)
    if self.time:
      elem.set("time", self.time)
    if self.is_preferred_contact != None:
      elem.set("preferredcontact", str(int(self.is_preferred_contact)))
    
    return elem


class Address:
  def __init__(self):
    self.address_type = None
    self.streets = []
    self.apartment = None
    self.city = None
    self.regioncode = None
    self.postalcode = None
    self.country = None
   
  def set_type(self, new_type: Literal["work", "home", "delivery"]):
    # NOTE: this is technically duplication. I think it's small enough to be fine but it may need to be changed later
    valid_types = ["work", "home", "delivery"]

    if not new_type in valid_types:
      raise ValueError("must have a valid type")
    
    self.address_type = new_type
    return self

  # TODO: for now adding them in order is probably fine
  # but going forward this needs to be more ergonomic for consumers
  def add_street(self, street_name: str):
    self.streets.append(street_name)
    return self
   
  def set_apartment(self, apartment: str):
    self.apartment = apartment
    return self
  
  def set_city(self, city: str):
    self.city = city
    return self
  
  # TODO: input validation would be nice
  def set_regioncode(self, regioncode: str):
    self.regioncode = regioncode
    return self
  
  def set_postalcode(self, postalcode: str):
    self.postalcode = postalcode
    return self

  # TODO: input validation would be nice 
  def set_country(self, country: str):
    self.country = country
    return self
  
  def to_xml(self):
    elem = etree.Element("address")

    if self.address_type:
       elem.set("type", self.address_type)

    for i, v in enumerate(self.streets):
       s = etree.SubElement(elem, "street")
       s.text = v
       s.set("line", str(i + 1))

    if self.apartment:
      a = etree.SubElement(elem, "apartment")
      a.text = self.apartment

    if self.city:
      c = etree.SubElement(elem, "city")
      c.text = self.city
    
    if self.regioncode:
      r = etree.SubElement(elem, "regioncode")
      r.text = self.regioncode

    if self.postalcode:
      p = etree.SubElement(elem, "postalcode")
      p.text = self.postalcode

    if self.country:
      c = etree.SubElement(elem, "country")
      c.text = self.country

    return elem


class Price:
    def __init__(self, value: str | int | float):
        self.value = str(value)
        self.type = None
        self.currency = None
        self.delta = None
        self.relativeto = None
        self.source = None

    def set_type(self, type: Literal["quote", "offer", "msrp", "invoice", "call", "appraisal", "asking"]):
        # NOTE: this is technically duplication. I think it's small enough to be fine but it may need to be changed later
        valid_types = ["quote", "offer", "msrp", "invoice", "call", "appraisal", "asking"]

        if not type in valid_types:
          raise ValueError("must have a valid type")

        self.type = type
        return self
    
    def set_currency(self, currency: Currency | str):
        if type(currency) == str:
          # attempt to parse the value
          cur = Currency(currency.upper())
          self.currency = cur.value
        else:
          self.currency = currency.value
        return self
    
    def set_delta(self, delta: Literal["absolute", "relative", "percentage"]):
      #  NOTE: this is technically duplication. I think it's small enough to be fine but it may need to be changed later
      valid_deltas = ["absolute", "relative", "percentage"]

      if not delta in valid_deltas:
         raise ValueError("must have a valid delta")

      self.delta = delta
      return self
    
    def set_relativeto(self, relativeto: Literal["msrp", "invoice"]):
      #  NOTE: this is technically duplication. I think it's small enough to be fine but it may need to be changed later
      valid_relativetos = ["msrp", "invoice"]

      if not relativeto in valid_relativetos:
         raise ValueError("must have a valid relativeto attribute")
      
      self.relativeto = relativeto
      return self
    
    def set_source(self, source: str):
       self.source = source
       return self
    
    def to_xml(self):
        elem = etree.Element("price")
        elem.text = self.value

        if self.type:
           elem.set("type", self.type)
        if self.currency:
           elem.set("currency", self.currency)
        if self.delta:
           elem.set("delta", self.delta)
        if self.relativeto:
           elem.set("relativeto", self.relativeto)
        if self.source:
           elem.set("source", self.source)
        
        return elem



class Id:
  def __init__(self, value: str):
    self.value = value
    self.sequence = None
    self.source = None

  def set_sequence(self, sequence: str):
    self.sequence = sequence
    return self
  
  def set_source(self, source: str):
    self.source = source
    return self

  def to_xml(self) :
    elem = etree.Element("id")
    if self.sequence:
      elem.set("sequence", self.sequence)
    if self.source:
      elem.set("source", self.source)

    elem.text = self.value

    return elem




class Contact:
  def __init__(self):
    self.is_primary_contact = None
    self.names: List[Name] = []
    self.emails: List[Email] = []
    self.phone_numbers: List[PhoneNumber] = []
    self.addresses: List[Address] = []
  
  def set_primary_contact(self, is_primary_contact: bool):
    self.is_primary_contact = is_primary_contact
    return self

  def add_name(self, name: Name):
    self.names.append(name)
    return self
  
  def add_email(self, email: Email):
    self.emails.append(email)
    return self
  
  def add_phone_number(self, phone_number: PhoneNumber):
    self.phone_numbers.append(phone_number)
    return self
  
  def add_address(self, address: Address):
    self.addresses.append(address)
    return self
  
  def to_xml(self):
    if len(self.names) == 0:
      raise ValueError("contact must have at least one name")
    
    elem = etree.Element("contact")

    if self.is_primary_contact != None:
      elem.set("primarycontact", str(int(self.is_primary_contact)))

    for n in self.names:
      elem.append(n.to_xml())

    for e in self.emails:
      elem.append(e.to_xml())

    for p in self.phone_numbers:
      elem.append(p.to_xml())
    
    for a in self.addresses:
       elem.append(a.to_xml())



    return elem
       



class Vehicle:
  
  __interest_attr: Literal["buy", "lease", "sell", "trade-in", "test-drive"] | None
  __status_attr: Literal["new", "used"] | None
  __id: Id | None
  __year: str
  __make: str
  __model: str
  __vin: str | None
  __stock: str | None
  __trim: str | None
  __doors: str | None
  __bodystyle: str | None
  __transmission: str | None
  __odometer: str | None
  __odometer_status_attr: Literal["unknown", "rolledover", "replaced", "original"] | None
  # NOTE: according to the spec, the only allowed options are mi and km, but the example breaks this (using "miles")
  # requires further investigation
  __odometer_units_attr: Literal["mi", "km"] | None
  __condition: Literal["excellent", "good", "fair", "poor", "unknown"] | None
  __color_combinations: List[Dict]
  __imagetag: Dict
  __price: Price | None
  __pricecomments: str | None
  __options: List[Dict]
  __finance: Dict
  __comments: str | None


  
  def __init__(self, year: str | int, make: str, model: str):
    self.__year = str(year)
    self.__make = make
    self.__model = model

    self.__interest_attr = None
    self.__status_attr = None
    self.__id = None
    self.__vin = None
    self.__stock = None
    self.__trim = None
    self.__doors = None
    self.__bodystyle = None
    self.__transmission = None
    self.__odometer = None
    self.__odometer_status_attr = None
    self.__odometer_units_attr = None
    self.__condition = None
    self.__color_combinations = []
    self.__imagetag = {}
    self.__price = None
    self.__pricecomments = None
    self.__options = []
    self.__finance = {}
    self.__comments = None


  def set_interest(self,  interest: Literal["buy", "lease", "sell", "trade-in", "test-drive"]):
    # NOTE: this is technically duplication. I think it's small enough to be fine but it may need to be changed later
    valid_interest_values = ["buy", "lease", "sell", "trade-in", "test-drive"]

    if not interest in valid_interest_values:
      raise ValueError("interest must be a valid value")
      
    self.__interest_attr = interest
    return self

  def set_status(self, status: Literal["new", "used"]):
    # NOTE: this is technically duplication. I think it's small enough to be fine but it may need to be changed later
    valid_statuses = ["new", "used"]

    if not status in valid_statuses:
      raise ValueError("status must be a valid value")
    
    self.__status_attr = status
    return self

  def set_id(self, id: Id):
    self.__id = id
    return self

  def set_vin(self, vin: str):
    self.__vin = vin
    return self
  
  def set_stock(self, stock: str):
    self.__stock = stock
    return self
  
  def set_trim(self, trim: str):
    self.__trim = trim
    return self
  
  def set_doors(self, doors: str):
    self.__doors = doors
    return self
  
  def set_bodystyle(self, bodystyle: str):
    self.__bodystyle = bodystyle
    return self
  
  def set_transmission(self, transmission: str):
    self.__transmission = transmission
    return self
  
  def set_odometer(self, odometer: str):
    self.__odometer = odometer
    return self
  
  def set_odometer_status(self, status: Literal["unknown", "rolledover", "replaced", "original"]):
    # NOTE: this is technically duplication. I think it's small enough to be fine but it may need to be changed later
    valid_statuses = ["unknown", "rolledover", "replaced", "original"]

    if not status in valid_statuses:
      raise ValueError("must have a valid status")
    
    self.__odometer_status_attr = status
    return self
  

  def set_odometer_units(self, unit: Literal["mi", "km"]):
    # NOTE: this is technically duplication. I think it's small enough to be fine but it may need to be changed later
    valid_units = ["mi", "km"]

    if not unit in valid_units:
      raise ValueError("must have a valid unit")
    
    self.__odometer_units_attr = unit
    return self


  def set_condition(self, condition: Literal["excellent", "good", "fair", "poor", "unknown"]):
    # NOTE: this is technically duplication. I think it's small enough to be fine but it may need to be changed later
    valid_conditions = ["excellent", "good", "fair", "poor", "unknown"]

    if not condition in valid_conditions:
      raise ValueError("must have a valid condition")
    
    self.__condition = condition
    return self


  def add_color_combination(self, interior_color: str | None, exterior_color: str | None, preference: int | None):
    new_color_combo = {
      "interiorcolor": interior_color,
      "exteriorcolor": exterior_color,
      "preference": str(preference),
    }

    self.__color_combinations.append(new_color_combo)
    return self

  # TODO: needs more value checking
  def set_imagetag(self, image_url: str, width: int | None, height: int | None, alt_text: str | None):
    self.__imagetag = {
      "url": image_url,
      "width": width,
      "height": height,
      "alttext": alt_text,
    }
    return self

  def set_price(self, price: Price):
    self.__price = price
    return self
  
  def set_price_comment(self, comment: str):
    self.__pricecomments = comment
    return self

  def add_option(self, 
                 option_name: str, 
                 manufacturer_code: str | None, 
                 stock_number: str | None,
                 weighting: int | None,
                 price: Price | None
  ):
    # TODO: doing it this way makes checking for valid types in to_xml() more cumbersome than it should be
    # those additional checks should be done here
    new_option = {
      "optionname": option_name,
      "manufacturercode": manufacturer_code,
      "stock": stock_number,
      "weighting": str(weighting),
      "price": price
    }

    self.__options.append(new_option)
    return self

  # TODO: this is kinda awful, could be really improved
  def set_finance(self, 
                  method: Literal["cash", "finance", "lease"],
                  amounts: List[Dict], # TODO: this needs to be done better
                  balance: Dict,
  ):
    self.__finance = {
      "method": method,
      "amounts": amounts,
      "balance": balance,
    }
    return self


  def set_comments(self, comments: str):
    self.__comments = comments
    return self





  def to_xml(self):
    elem = etree.Element("vehicle")

    if self.__interest_attr:
      elem.set("interest", self.__interest_attr)
    
    if self.__status_attr:
      elem.set("status", self.__status_attr)

    if self.__id:
      elem.append( self.__id.to_xml() )

    y = etree.SubElement(elem, "year")
    y.text = self.__year

    ma = etree.SubElement(elem, "make")
    ma.text = self.__make

    mo = etree.SubElement(elem, "model")
    mo.text = self.__model


    if self.__vin:
      v = etree.SubElement(elem, "vin")
      v.text = self.__vin
    
    if self.__stock:
      s = etree.SubElement(elem, "stock")
      s.text = self.__stock
    
    if self.__trim:
      t = etree.SubElement(elem, "trim")
      t.text = self.__trim

    if self.__doors:
      d = etree.SubElement(elem, "doors")
      d.text = self.__doors
    
    if self.__bodystyle:
      b = etree.SubElement(elem, "bodystyle")
      b.text = self.__bodystyle
    
    if self.__transmission:
      t = etree.SubElement(elem, "transmission")
      t.text = self.__transmission

    if self.__odometer:
      o = etree.SubElement(elem, "odometer")
      o.text = self.__odometer

      if self.__odometer_status_attr:
        o.set("status", self.__odometer_status_attr)
      
      if self.__odometer_units_attr:
        o.set("units", self.__odometer_units_attr)
      
    if self.__condition:
      c = etree.SubElement(elem, "condition")
      c.text = self.__condition
    
    for combo in self.__color_combinations:
      c = etree.SubElement(elem, "colorcombination")
      if "interiorcolor" in combo:
        i = etree.SubElement(c, "interiorcolor")
        i.text = combo["interiorcolor"]
      
      if "exteriorcolor" in combo:
        e = etree.SubElement(c, "exteriorcolor")
        e.text = combo["exteriorcolor"]
      
      if "preference" in combo:
        p = etree.SubElement(c, "preference")
        p.text = combo["preference"]
      
    if len(self.__imagetag) != 0:
      i = etree.SubElement(elem, "imagetag")
      i.text = self.__imagetag["url"]

      if "width" in self.__imagetag:
        i.set("width", self.__imagetag["width"])
      
      if "height" in self.__imagetag:
        i.set("height", self.__imagetag["height"])
      
      if "alttext" in self.__imagetag:
        i.set("alttext", self.__imagetag["alttext"])
      
    if self.__price:
      elem.append(self.__price.to_xml())
    
    if self.__pricecomments:
      p = etree.SubElement(elem, "pricecomments")
      p.text = self.__pricecomments
    
    for option in self.__options:
      o = etree.SubElement(elem, "option")

      if "optionname" in option:
        n = etree.SubElement(o, "optionname")
        n.text = option["optionname"]
      
      if "manufacturercode" in option:
        c = etree.SubElement(o, "manufacturercode")
        c.text = option["manufacturercode"]
      
      if "stock" in option:
        s = etree.SubElement(o, "stock")
        s.text = option["stock"]
      
      if "weighting" in option:
        w = etree.SubElement(o, "weighting")
        w.text = option["weighting"]
      
      if "price" in option:
        o.append( option["price"].to_xml() )
      
    if len(self.__finance) != 0:
      f = etree.SubElement(elem, "finance")

      if "method" in self.__finance:
        m = etree.SubElement(f, "method")
        m.text = self.__finance["method"]

      for amount in self.__finance["amounts"]:
        a = etree.SubElement(f, "amount")
        a.text = str(amount["amount"])

        if "type" in amount:
          a.set("type", amount["type"])
        
        if "currency" in amount:
          a.set("currency", amount["currency"])

      if "balance" in self.__finance:
        b = etree.SubElement(f, "balance")
        b.text = str(self.__finance["balance"]["balance"])
        b.set("type", self.__finance["balance"]["type"])
        b.set("currency", self.__finance["balance"]["currency"])

    if self.__comments:
      c = etree.SubElement(elem, "comments")
      c.text = self.__comments
    
      



    return elem



class Customer:
    
    __contact: Contact
    __id: Id | None
    __comments: str | None
    __timeframe : Dict

    def __init__(self, contact: Contact):
      self.__contact = contact
      self.__id = None
      self.__comments = None
      self.__timeframe = {}

    def set_id(self, id: Id):
      self.__id = id
      return self
    
    def set_comments(self, comments: str):
      self.__comments = comments
      return self
    
    def set_timeframe(self, earliest_date: datetime | None, latest_date: datetime | None, description: str | None):
      self.__timeframe["earliestdate"] = earliest_date
      self.__timeframe["latestdate"] = latest_date
      self.__timeframe["description"] = description
      return self


    def to_xml(self):
      elem = etree.Element("customer")

      elem.append( self.__contact.to_xml() )

      if self.__id:
        elem.append(self.__id.to_xml())
      
      if len(self.__timeframe) != 0:
        # TODO: the adf spec says that this is a requirement, but in the same document they break this requirement
        # needs further investigation
        if self.__timeframe["earliestdate"] == None or self.__timeframe["latestdate"] == None:
          raise ValueError("if timeframe tag is present, it is required to specify earliestdate and/or latestdate")

        t = etree.SubElement(elem, "timeframe")

        if "earliestdate" in self.__timeframe:
          ed = etree.SubElement(t, "earliestdate")
          ed.text = self.__timeframe["earliestdate"].replace(microsecond=0).isoformat()
        
        if "latestdate" in self.__timeframe:
          ld = etree.SubElement(t, "latestdate")
          ld.text = self.__timeframe["latestdate"].replace(microsecond=0).isoformat()

        if "description" in self.__timeframe:
          d = etree.SubElement(t, "description")
          d.text = self.__timeframe["description"]

      
      if self.__comments:
        c = etree.SubElement(elem, "comments")
        c.text = self.__comments


      return elem

class Vendor:
    
    __id: Id | None
    __vendor_name: str
    __url: str | None
    __contact: Contact

    def __init__(self, vendor_name: str, contact: Contact):
      self.__vendor_name = vendor_name
      self.__contact = contact
      self.__id = None
      self.__url = None

    def set_id(self, id: Id):
      self.__id = id
      return self
    
    def set_url(self, url: str):
      self.__url = url
      return self
    
    def to_xml(self):
      elem = etree.Element("vendor")

      if self.__id:
        elem.append(self.__id.to_xml())

      vn = etree.SubElement(elem, "vendorname")
      vn.text = self.__vendor_name

      if self.__url:
        u = etree.SubElement(elem, "url")
        u.text = self.__url

      elem.append(self.__contact.to_xml())

      return elem


class Provider:
  def __init__(self):
    self.id: Id | None = None
    self.names: List[Name] = []
    self.service: str | None = None
    self.url: str | None = None
    self.emails: List[Email] = []
    self.phone_numbers: List[PhoneNumber] = []
    self.contact: Contact | None = None

  def set_id(self, id: Id):
    self.id = id
    return self

  def add_name(self, name: Name):
    self.names.append(name)
    return self
  
  def set_service(self, service: str):
    self.service = service
    return self
  
  def set_url(self, url: str):
    self.url = url
    return self
  
  def add_email(self, email: Email):
    self.emails.append(email)
    return self
  
  def add_phone_number(self, phone_number: PhoneNumber):
    self.phone_numbers.append(phone_number)
    return self

  def set_contact(self, contact: Contact):
    self.contact = contact
    return self

  def to_xml(self):
    
    if len(self.names) == 0:
      raise ValueError("must have at least one name")

    elem = etree.Element("provider")


    if self.id:
      elem.append( self.id.to_xml() )

    for n in self.names:
      elem.append(n.to_xml())

    if self.service:
      s = etree.SubElement(elem, "service")
      s.text = self.service

    if self.url:
      u = etree.SubElement(elem, "url")
      u.text = self.url

    for e in self.emails:
      elem.append(e.to_xml())

    for p in self.phone_numbers:
      elem.append(p.to_xml())
    

    if self.contact:
      elem.append(self.contact.to_xml())

    return elem







class Prospect:

    __id: Id | None
    __request_date: datetime | None
    __vehicles: List[Vehicle]
    __customer: Customer | None
    __vendor: Vendor | None
    __provider: Provider | None

    def __init__(self):
      self.__id = None
      self.__request_date = None
      self.__vehicles = []
      self.__customer = None
      self.__vendor = None
      self.__provider = None

    def set_id(self, id: Id):
      self.__id = id
      return self

    def set_request_date(self, requestdate: datetime):
      self.__request_date = requestdate
      return self

    def add_vehicle(self, vehicle: Vehicle):
      self.__vehicles.append(vehicle)
      return self
    
    def set_customer(self, customer: Customer):
      self.__customer = customer
      return self
    
    def set_vendor(self, vendor: Vendor):
      self.__vendor = vendor
      return self
    
    def set_provider(self, provider: Provider):
      self.__provider = provider
      return self
    
    def to_xml(self):
      elem = etree.Element("prospect")

      if self.__id:
        elem.append(self.__id.to_xml())

      if self.__request_date:
        r = etree.SubElement(elem, "requestdate")
        r.text = self.__request_date.replace(microsecond=0).isoformat()
      
      for vehicle in self.__vehicles:
        elem.append(vehicle.to_xml())
      
      if self.__customer:
        elem.append(self.__customer.to_xml())
      
      if self.__vendor:
        elem.append(self.__vendor.to_xml())

      if self.__provider:
        elem.append(self.__provider.to_xml())
      
      return elem





class Adf:
    
    __prospect: Prospect

    def __init__(self, prospect: Prospect):
        self.__prospect = prospect

    @staticmethod
    def from_xml_str(xml: str):
      pass
    
    def to_xml(self):
      elem = etree.Element("adf")

      elem.append(self.__prospect.to_xml())

      return elem

    


