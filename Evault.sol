pragma solidity >= 0.8.11 <= 0.8.11;
pragma experimental ABIEncoderV2;
//evault solidity code
contract Evault {

    uint public documentCount = 0; 
    mapping(uint => document) public documentList; 
     struct document
     {
       string document_name;
       string document_type;
       string description;
       string document_belongs_to;
       string doc_address;
       string phone;
       string criminal_record;
       string uid;
       string update_date;
       string filename;
     }
 
   // events 
   event documentCreated(uint indexed _documentId);
   
   //function  to save legal document details to Blockchain
   function saveDocument(string memory name, string memory doc_type, string memory desc, string memory belongs, string memory doc_address, string memory phone, string memory criminal_record,  string memory uid,  string memory update_date, string memory filename) public {
      documentList[documentCount] = document(name, doc_type, desc, belongs, doc_address, phone, criminal_record, uid, update_date, filename);
      emit documentCreated(documentCount);
      documentCount++;
    }

     //get document count
    function getDocumentCount()  public view returns (uint) {
          return  documentCount;
    }

    function getName(uint i) public view returns (string memory) {
        document memory doc = documentList[i];
	return doc.document_name;
    }

    function getType(uint i) public view returns (string memory) {
        document memory doc = documentList[i];
	return doc.document_type;
    }

    function getDesc(uint i) public view returns (string memory) {
        document memory doc = documentList[i];
	return doc.description;
    }

    function getBelongs(uint i) public view returns (string memory) {
        document memory doc = documentList[i];
	return doc.document_belongs_to;
    }

    function getAddress(uint i) public view returns (string memory) {
        document memory doc = documentList[i];
	return doc.doc_address;
    }

    function getPhone(uint i) public view returns (string memory) {
        document memory doc = documentList[i];
	return doc.phone;
    }

    function getCriminalRecord(uint i) public view returns (string memory) {
        document memory doc = documentList[i];
	return doc.criminal_record;
    }

    function getUid(uint i) public view returns (string memory) {
        document memory doc = documentList[i];
	return doc.uid;
    }

    function getDate(uint i) public view returns (string memory) {
        document memory doc = documentList[i];
	return doc.update_date;
    }

    function getFile(uint i) public view returns (string memory) {
        document memory doc = documentList[i];
	return doc.filename;
    }
}