# 4. Design boundaries

Load `architect` when a change crosses a meaningful function, module, process, storage, or network boundary. Start from the caller and settle the data shape, ownership, lifecycle, and invalid states before implementation.

For uncertain designs, use `arena` or `prototype`: compare materially different options against one frozen rubric. True isolated workers are preferred when the host supports them. Sequential alternatives remain useful, but they are not independent evidence.
