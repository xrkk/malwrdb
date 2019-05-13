class PeSample {
    _id: string;
}

class PeValueStructure {
  name: string;
  offset_file: number;
  offset_mm: number;
  value: string;
}

class PeSection{
  Characteristics: string;
  Misc: string;
  Misc_PhysicalAddress: string;
  Misc_VirtualSize: string;
  Name: string;
  NumberOfLinenumbers: string;
  NumberOfRelocations: string;
  PointerToLinenumbers: string;
  PointerToRawData: string;
  PointerToRelocations: string;
  SizeOfRawData: string;
  VirtualAddress: string;
}

class PeImportDllItem{
  ordinal: number;
  name: string;
  bound: string;
}

class PeImportDllTable{
  dll_name: string;
  item_list: Array<PeImportDllItem>;
  value_dict: Array<PeValueStructure>;
}



export { PeSample, PeValueStructure, PeSection, PeImportDllItem, PeImportDllTable }