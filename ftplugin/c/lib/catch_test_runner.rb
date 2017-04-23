
module ACR #Auro Catch Runner
    def ACR.run(filename, line_number)

        # parse filename -> get submodule, test_case tag, [section name, [nested section name]]
        # build target and parse output
        # if error -> construct result and exit
        # run test [tag1][tag2] (or run test -c section_name) and parse output
        # if error -> construct result and exit
        # else return empty dictionary/hash


        # example result

        column_number = 14
        result_list = []
        list_item = {filename: "#{filename}",
                     lnum: line_number,
                     col: column_number,
                     text: "Description",
                     type: 'W'  #error type: in the docs, literally: "single-character error type, 'E', 'W', etc." no clue where to find the etc. part
                    }
        result_list << list_item

        return result_list
    end
end
