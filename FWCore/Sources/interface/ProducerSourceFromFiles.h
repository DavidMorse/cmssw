#ifndef FWCore_Sources_ProducerSourceFromFiles_h
#define FWCore_Sources_ProducerSourceFromFiles_h

/*----------------------------------------------------------------------
----------------------------------------------------------------------*/

#include <string>
#include <vector>

#include "FWCore/Sources/interface/FromFiles.h"
#include "FWCore/Sources/interface/ProducerSourceBase.h"

namespace edm {
  class ParameterSet;
  class ParameterSetDescription;

  class ProducerSourceFromFiles : public ProducerSourceBase, private FromFiles {
  public:
    ProducerSourceFromFiles(ParameterSet const& pset, InputSourceDescription const& desc, bool realData);
    virtual ~ProducerSourceFromFiles();

    using FromFiles::logicalFileNames;
    using FromFiles::fileNames;
    using FromFiles::catalog;
    
    static void fillDescription(ParameterSetDescription& desc);

  protected:
    using FromFiles::incrementFileIndex;

  private:
    using FromFiles::noFiles;
    using FromFiles::fileIndex;
  };
}
#endif
